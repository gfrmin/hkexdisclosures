# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TransactionNotice(scrapy.Item):
    # magic fields
    timestamp = scrapy.Field()
    url = scrapy.Field()
    
    # main details 
    formtype = scrapy.Field()
    formserialnumber = scrapy.Field()

    corporation = scrapy.Field()
    stock_code = scrapy.Field()
    assetclass = scrapy.Field()
    number_issued = scrapy.Field()

    surname = scrapy.Field()
    othernames = scrapy.Field()
    chinesename = scrapy.Field()
    chinesecharactercode = scrapy.Field()

    name = scrapy.Field()
    registeredoffice = scrapy.Field()
    principalplace = scrapy.Field()
    listedexchange = scrapy.Field()
    parentdetails = scrapy.Field()

    associatedcorporation = scrapy.Field()
    brnumber = scrapy.Field()
    certincorpnumber = scrapy.Field()
    placeincorp = scrapy.Field()

    date = scrapy.Field()
    dateaware = scrapy.Field()

    # event details
    
    relevanteventdetails = scrapy.Field()

    before = scrapy.Field()
    after = scrapy.Field()

    capacityheld = scrapy.Field()

    # further information
    
    derivativeinterests = scrapy.Field()

    dependentinformation = scrapy.Field()

    othercorporationinterests = scrapy.Field()

    jointinterests = scrapy.Field()

    trustinterests = scrapy.Field()

    s317info = scrapy.Field()
    s317total = scrapy.Field()

    accordancepersons = scrapy.Field()

    debenturerights = scrapy.Field()
    

    # final details

    dateformfilled = scrapy.Field()

    numberofattachments = scrapy.Field()

    supplementaryinfo = scrapy.Field()

    previousserialnumber = scrapy.Field()




