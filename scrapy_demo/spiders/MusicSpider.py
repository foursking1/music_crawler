#-*- coding: utf-8 -*-
import scrapy
from scrapy_webdriver.http import WebdriverRequest
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from items import MusicInfo
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class MusicSpider(scrapy.Spider):
    name = "MusicSpider"
    logging.getLogger("MusicSpider").setLevel(logging.WARNING)

    def start_requests(self):
        url = "http://music.163.com/#/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=0"
        #url = "http://music.163.com/#/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=1435"
        yield WebdriverRequest(url, callback=self.parse_page)

    def parse_page(self, response):
        try:
            driver = response.webdriver
            driver.switch_to.frame("g_iframe")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul#m-pl-container "))
            )
            page_source = driver.page_source
            bs_obj = BeautifulSoup(page_source, "lxml")
            elements = bs_obj.select("ul#m-pl-container > li > p.dec > a")
            for ele in elements:
                playlist =  "http://music.163.com/#" + ele["href"]
                yield WebdriverRequest(playlist, callback=self.parse_list)

            next_page = bs_obj.select("a.znxt.js-disabled")
            if not next_page:
                next_page_url = "http://music.163.com/#" + bs_obj.select("a.znxt")[0]['href']
                print next_page_url
                yield WebdriverRequest(next_page_url, callback=self.parse_page)

        except Exception, e:
            self.logger.error(e)

    def parse_list(self, response):
        try:
            driver = response.webdriver
            driver.switch_to.frame("g_iframe")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#m-playlist"))
            )
            # \33 55669911486619025162 > td:nth-child(2) > div > div > div > span > a > b
            page_source = driver.page_source
            bs_obj = BeautifulSoup(page_source, "lxml")
            elements = bs_obj.select("div#m-playlist div.n-songtb table tbody tr")
            for ele in elements:
                music_info = MusicInfo()
                url = "http://music.163.com" + ele.select("td")[1].find("a")['href']
                title = ele.select("td")[1].find("a").text
                singer = ele.select("td")[3].text
                album = ele.select("td")[4].text
                id = url.split('=')[1]
                music_info["_id"] = id
                music_info["title"] = title
                music_info["singer"] = singer
                music_info["album"] = album
                music_info["url"] = url
                yield music_info


        except Exception, e:
            self.logger.error(e)
