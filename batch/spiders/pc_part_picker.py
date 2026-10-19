"""Selenium-backed PCPartPicker GPU trend-image collector."""

import json
import shutil
import tempfile
import time
from pathlib import Path

import scrapy
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
        self.driver = uc.Chrome(options=options)

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
