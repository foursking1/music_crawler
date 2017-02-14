#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from items import MusicInfo
from items import PlaylistInfo
import json


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.music_file = open('items.jl', 'w')
        self.playlist_file = open('playlist', 'w')

    def close_spider(self, spider):
        self.music_file.close()
        self.playlist_file.close()


    def process_item(self, item, spider):
        if isinstance(item, MusicInfo):
            line = json.dumps(dict(item)) + "\n"
            self.music_file.write(line)
        if isinstance(item, PlaylistInfo):
            line = json.dumps(dict(item)) + "\n"
            self.playlist_file.write(line)
        return item
