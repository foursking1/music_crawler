#-*- coding: utf-8 -*-
import scrapy
from scrapy_webdriver.http import WebdriverRequest
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapy_demo.items import MusicInfo
from scrapy_demo.items import PlaylistInfo
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')


class MusicSpider(scrapy.Spider):
    name = "MusicSpider"
    logging.getLogger("MusicSpider").setLevel(logging.WARNING)

    def start_requests(self):
        urls = ["http://music.163.com/#/discover/playlist/?cat=清晨&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=夜晚&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=学习&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=工作&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=午休&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=下午茶&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=地铁&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=驾车&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=运动&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=旅行&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=散步&order=hot",
                "http://music.163.com/#/discover/playlist/?cat=酒吧&order=hot"]
        
        for url in urls:
            yield WebdriverRequest(url, callback=self.parse_page)

        # url = "http://music.163.com/#/discover/playlist/?cat=清晨&order=hot"
        # yield WebdriverRequest(url, callback=self.parse_page)

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
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#m-playlist div.n-songtb table tbody tr"))
            )

            # \33 55669911486619025162 > td:nth-child(2) > div > div > div > span > a > b
            page_source = driver.page_source
            bs_obj = BeautifulSoup(page_source, "lxml")
            elements = bs_obj.select("div#m-playlist div.n-songtb table tbody tr")
            play_list_id = response.url.split('=')[1]

            for ele in elements:
                try:
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
                    music_info['pid'] = play_list_id
                    yield music_info
                except:
                    continue


            id = play_list_id
            name = bs_obj.select_one("div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.hd.f-cb > div > h2").text
            times = bs_obj.select_one("div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.user.f-cb > span.time.s-fc4").text.split(" ")[0]
            tag = bs_obj.select_one("div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.tags.f-cb").text.replace('\n', ' ')
            introduction = bs_obj.select_one("#album-desc-more").text
            author = bs_obj.select_one("div.g-mn4 > div > div > div.m-info.f-cb > div.cnt > div > div.user.f-cb > span.name > a").text
            play_times = bs_obj.select_one("#play-count").text
            share_times = bs_obj.select_one("#content-operation > a.u-btni.u-btni-share > i").text.replace('(', '').replace(')', '')
            collect_times = bs_obj.select_one("#content-operation > a.u-btni.u-btni-fav > i").text.replace('(', '').replace(')', '')
            comments_times = bs_obj.select_one("#cnt_comment_count").text
            play_list_info = PlaylistInfo()
            play_list_info["_id"] = id
            play_list_info["Name"] = name
            play_list_info["Time"] = times
            play_list_info["Tag"] = tag
            play_list_info["Author"] = author
            play_list_info["Introduction"] = introduction
            play_list_info["Playnum"] = play_times
            play_list_info["Sharenum"] = share_times
            play_list_info["Collectnum"] = collect_times
            play_list_info["Commentnum"] = comments_times
            yield play_list_info


        except Exception, e:
            self.logger.error(e)
            traceback.print_exc()
