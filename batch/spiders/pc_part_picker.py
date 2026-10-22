"""Selenium-backed PCPartPicker GPU trend-image collector."""

import json
import ctypes
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import scrapy
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _parse_chrome_major_version(version_output):
    """Return Chrome's major version from ``chrome.exe --version`` output."""
    match = re.search(r"(?:Chrome|Chromium)\s+(\d+)", version_output or "")
    return int(match.group(1)) if match else None


def _detect_chrome_major_version():
    """Detect the installed Chrome major version for driver compatibility."""
    candidates = [
        shutil.which("chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES", ""), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(
            os.environ.get("PROGRAMFILES(X86)", ""),
            "Google",
            "Chrome",
            "Application",
            "chrome.exe",
        ),
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"
        ),
    ]
    for candidate in dict.fromkeys(path for path in candidates if path):
        if not Path(candidate).exists():
            continue
        file_major = _windows_file_major_version(candidate)
        if file_major is not None:
            return file_major
        try:
            result = subprocess.run(
                [candidate, "--version"],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        major = _parse_chrome_major_version(result.stdout or result.stderr)
        if major is not None:
            return major
    return None


def _windows_file_major_version(path):
    """Read a Windows executable's major file-version without starting it."""
    if os.name != "nt":
        return None
    try:
        from ctypes import wintypes

        version_dll = ctypes.WinDLL("version", use_last_error=True)
        version_dll.GetFileVersionInfoSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
        version_dll.GetFileVersionInfoSizeW.restype = wintypes.DWORD
        version_dll.GetFileVersionInfoW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
        ]
        version_dll.GetFileVersionInfoW.restype = wintypes.BOOL
        version_dll.VerQueryValueW.argtypes = [
            wintypes.LPVOID,
            wintypes.LPCWSTR,
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(wintypes.UINT),
        ]
        version_dll.VerQueryValueW.restype = wintypes.BOOL

        dummy = wintypes.DWORD()
        size = version_dll.GetFileVersionInfoSizeW(path, ctypes.byref(dummy))
        if not size:
            return None
        data = ctypes.create_string_buffer(size)
        if not version_dll.GetFileVersionInfoW(path, 0, size, data):
            return None
        value = ctypes.c_void_p()
        length = wintypes.UINT()
        if not version_dll.VerQueryValueW(data, "\\", ctypes.byref(value), ctypes.byref(length)):
            return None

        class FixedFileInfo(ctypes.Structure):
            _fields_ = [
                ("dwSignature", wintypes.DWORD),
                ("dwStrucVer", wintypes.DWORD),
                ("dwFileVerMS", wintypes.DWORD),
                ("dwFileVerLS", wintypes.DWORD),
            ]

        info = ctypes.cast(value, ctypes.POINTER(FixedFileInfo)).contents
        return info.dwFileVerMS >> 16
    except (AttributeError, OSError, TypeError, ValueError):
        return None


class PCPartPickerGPUSpider(scrapy.Spider):
    name = "pcpartpicker_gpu_trends"
    allowed_domains = ["pcpartpicker.com"]

    def __init__(
        self,
        start_url="https://pcpartpicker.com/trends/price/video-card/",
        output_file="pcpartpicker_gpu_trends.json",
        headless="false",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.start_url = start_url
        self.output_file = Path(output_file)
        options = uc.ChromeOptions()
        if str(headless).lower() == "true":
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        chrome_major = _detect_chrome_major_version()
        driver_kwargs = {"options": options}
        if chrome_major is not None:
            self.logger.info("Using ChromeDriver major version %s", chrome_major)
            driver_kwargs["version_main"] = chrome_major
        else:
            self.logger.warning("Could not detect Chrome version; using driver auto-detection")
        self.driver = uc.Chrome(**driver_kwargs)

    def start_requests(self):
        """Run the browser collection once, then let Scrapy close cleanly."""
        self.logger.info("Opening PCPartPicker GPU trends page")
        try:
            self.driver.get(self.start_url)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.block img"))
            )
            self.scroll_to_bottom()
            self.parse_page()
        finally:
            self.driver.quit()
        return []

    def scroll_to_bottom(self, pause=1.5):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return
            last_height = new_height

    def parse_page(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        results = []
        seen = set()
        for block in soup.select("div.block"):
            h3 = block.find("h3")
            img = block.find("img")
            if not h3 or not img or not h3.contents:
                continue
            gpu_model = h3.contents[0].strip()
            image_url = img.get("src", "").strip()
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            if not gpu_model or not image_url.startswith(("http://", "https://")):
                self.logger.warning("Skipping incomplete GPU block")
                continue
            if gpu_model in seen:
                self.logger.warning("Skipping duplicate GPU model: %s", gpu_model)
                continue
            seen.add(gpu_model)
            results.append({"gpu_model": gpu_model, "image_url": image_url})

        self.logger.info("Extracted %d unique GPU trend images", len(results))
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        if self.output_file.exists():
            shutil.copy2(self.output_file, self.output_file.with_suffix(self.output_file.suffix + ".bak"))
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.output_file.parent, delete=False) as handle:
            json.dump(results, handle, indent=2)
            handle.write("\n")
            temp_path = Path(handle.name)
        temp_path.replace(self.output_file)
