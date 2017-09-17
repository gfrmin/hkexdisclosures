# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class notice(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    formID = scrapy.Field()
    StockCode = scrapy.Field()
    DateSSaware = scrapy.Field()
    eventDate = scrapy.Field()
    formType = scrapy.Field()
    nameOfListedCorporation = scrapy.Field()
    name = scrapy.Field()
    surname = scrapy.Field()
    othernames = scrapy.Field()
    numberofissuedshares = scrapy.Field()
    formDate = scrapy.Field()
    
    longpositionbefore = scrapy.Field()
    shortpositionbefore = scrapy.Field()
    lendingpoolbefore = scrapy.Field()    
    longpositionafter = scrapy.Field()
    shortpositionafter = scrapy.Field()
    lendingpoolafter = scrapy.Field()    
