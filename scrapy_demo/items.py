#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scrapy import Item, Field

class PlaylistInfo(Item):
    """歌单信息"""
    _id = Field()
    Name = Field()
    Time = Field()
    Tag = Field()
    Author = Field()
    Playtimes = Field()
    Sharetimes = Field()
    Collecttimes = Field()
    Commnets = Field()

class MusicInfo(Item):
    """音乐信息"""
    _id = Field()
    url = Field()
    title = Field()
    singer = Field()
    album = Field()