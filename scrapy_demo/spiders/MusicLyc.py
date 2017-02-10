#-*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time
import logging
from bs4 import BeautifulSoup
from scrapy_demo.items import MusicInfo
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class MusicLyc(scrapy.Spider):
    name = "MusicLycSpider"
    logging.getLogger("MusicSpider").setLevel(logging.WARNING)

    def start_requests(self):
        with open('songs.txt') as f:
            for song in f.readlines():
                url = "http://sou.kuwo.cn/ws/NSearch?type=all&key=" + song
                yield Request(url, callback=self.parse_page)
                break

    def parse_page(self, response):
        try:
            page_source = response.body
            bs_obj = BeautifulSoup(page_source, "lxml")
            url = bs_obj.select("#content > div > div > div.mainwrap.fl > div.m_list > form > div.list > ul > li")[0].select(" p.m_name > a")[0]['href']
            yield Request(url, callback=self.parse_song)

        except Exception, e:
            self.logger.error(e)

    def parse_song(self, response):
        try:
            page_source = response.body
            bs_obj = BeautifulSoup(page_source, "lxml")
            songs = ""
            for line in bs_obj.select("p.lrcItem"):
                songs += line.text + '\n'
            title = bs_obj.select_one("p.lrcName").text
            print title


        except Exception, e:
            self.logger.error(e)
