# -*- coding: utf-8 -*-
import scrapy
from hkexdisclosures.items import notice


class HkexspiderSpider(scrapy.Spider):
    name = "hkexspider"
    allowed_domains = ["sdinotice.hkex.com.hk"]
    start_urls = ['http://sdinotice.hkex.com.hk/filing/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/01/2003&sced=17/09/2017&sc=1&src=MAIN&lang=EN']

    def parse(self, response):
        for linkurl in response.css("a:nth-child(11)::attr(href)").extract():
            yield scrapy.Request(response.urljoin(linkurl), callback = self.parse_notices)

    def parse_notices(self, response):
        for linkurl in response.css("#grdPaging .tbCell:nth-child(1) a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(linkurl), callback = self.parse_notice)
        for pageurl in response.css("#lblPageIndex a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(pageurl), callback = self.parse_notices)
        
    def parse_notice(self, response):
        newnotice = notice()
        newnotice['url'] = response.url
        newnotice['formID'] = response.css("#lblDLogNo::text").extract_first()
        newnotice['StockCode'] = response.css("#lblDStockCode::text").extract_first()
        newnotice['DateSSaware'] = response.css("#lblDAwareDate::text").extract_first()
        newnotice['eventDate'] = response.css("#lblDEventDate::text").extract_first()
        newnotice['formType'] = response.css("#lblCaption::text").extract()
        newnotice['nameOfListedCorporation'] = response.css("#lblViewCorpName::text").extract_first()
        newnotice['name'] = response.css("#lblDName::text").extract_first()
        newnotice['directorLastName'] = response.css("#lblDSurname::text").extract()
        newnotice['directorFirstName'] = response.css("#lblDFirstname::text").extract()
       
        beforerowdict = {}
        for beforerow in response.css("#grdSh_BEvt tr")[1:]:
            beforerowstuff = beforerow.css("td::text").extract()
            beforerowdict[beforerowstuff[0]] = beforerowstuff[1]
        for key, value in beforerowdict.items():
            newnotice[key.replace(" ","").lower() + "before"] = value

        afterrowdict = {}
        for afterrow in response.css("#grdSh_AEvt tr")[1:]:
            afterrowstuff = afterrow.css("td::text").extract()
            afterrowdict[afterrowstuff[0]] = afterrowstuff[1]
        for key, value in afterrowdict.items():
            newnotice[key.replace(" ","").lower() + "after"] = value
            
        yield newnotice
