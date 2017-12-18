# -*- coding: utf-8 -*-
import scrapy
from hkexdisclosures.items import TransactionNotice

class HkexspiderSpiderOld(scrapy.Spider):
    name = "hkexspiderold"
    allowed_domains = ["sdinotice.hkex.com.hk", "www.hkexnews.hk"]
    start_urls = ['http://www.hkexnews.hk/listedco/listconews/advancedsearch/stocklist_active_main.htm']

    def parse(self, response):
        stockcodes = response.css(".TableContentStyle1 td:nth-child(1)::text , .TableContentStyle2 td:nth-child(1)::text").extract()
        stockurls = ['http://sdinotice.hkex.com.hk/filing/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/01/2003&sced=02/07/2017&sc='+sc+'&src=MAIN&lang=EN' for sc in stockcodes]
        for stockurl in stockurls:
            yield scrapy.Request(stockurl, callback = self.parse_searchresults)
    
    def parse_searchresults(self, response):
        try:
            for linkurl in response.css("a:nth-child(11)::attr(href)").extract():
                yield scrapy.Request(response.urljoin(linkurl), callback = self.parse_notices)
        except Error as e:
            pass

    def parse_notices(self, response):
        try:
            for linkurl in response.css("#grdPaging .tbCell:nth-child(1) a::attr(href)").extract():
                yield scrapy.Request(response.urljoin(linkurl), callback = self.parse_notice)
        except Error as e:
            pass
        else:
            for pageurl in response.css("#lblPageIndex a::attr(href)").extract():
                yield scrapy.Request(response.urljoin(pageurl), callback = self.parse_notices)
        
    def parse_notice(self, response):
        def extractminitable(classidcoderows, desc="Number of shares"):
            classidcoderowdict = {}
            for classidcoderow in classidcoderows:
                classidcoderowtds = classidcoderow.xpath("td//text()").extract()
                classidcoderowdict.update({classidcoderowtds[0]: classidcoderowtds[1]})
            return {desc: classidcoderowdict}
    
        def extractformtable(tableid, minitablep):
            field = []
            table = response.xpath('//*[(@id = ' + tableid + ')]/tr')
            if not table: return []
            tablecols = table[0].css("td::text").extract()
            tablerows = table[1:]
            tablecolsnumber = len(tablecols)
            for tablerow in tablerows:
                tablerowtds = tablerow.xpath("td")
                if minitablep:
                    minitable = extractminitable(tablerowtds[tablecolsnumber - 1].xpath("table/tr"))
                    tablerowdict = dict(zip(
                        tablecols,
                        [tablerowtds[x].css("::text").extract_first() for x in range(tablecolsnumber - 1)]
                    ))
                    tablerowdict.update(minitable)
                else:
                    tablerowdict = dict(zip(
                        tablecols,
                        [tablerowtds[x].css("::text").extract_first() for x in range(tablecolsnumber)]
                    ))
                field.append(tablerowdict)
            return field
        
        item = TransactionNotice()

        # main details
        
        item['formtype'] = response.css("#lblCaption::text").extract_first()
        item['formserialnumber'] = response.css("#lblDLogNo::text").extract_first()

        item['corporation'] = response.css("#lblViewCorpName::text").extract_first()
        item['stock_code'] = response.css("#lblDStockCode::text").extract_first()
        item['assetclass'] = response.css("#lblDClass::text").extract_first()
        item['number_issued'] = response.css("#lblDIssued::text").extract_first()

        item['surname'] = response.css("#lblDSurname::text").extract_first()
        item['othernames'] = response.css("#lblDFirstname::text").extract_first()
        item['chinesename'] = response.css("#lblDChiName::text").extract_first()
        item['chinesecharactercode'] = response.css("#lblDCharCode::text").extract_first()

        item['name'] = response.css("#lblDName::text").extract_first()
        item['registeredoffice'] = response.css("#lblDRegOffice::text").extract_first()
        item['principalplace'] = response.css("#lblDPrinPlace::text").extract_first()
        item['listedexchange'] = response.css("#lblDExList::text").extract_first()
        item['parentdetails'] = response.css("#lblDParent::text").extract_first()

        item['associatedcorporation'] = response.css("#lblDAssoCorpName::text").extract_first()
        item['brnumber'] = response.css("#lblDBusRegNo::text").extract_first()
        item['certincorpnumber'] = response.css("#lblViewCINo::text").extract_first()
        item['placeincorp'] = response.css("#lblDCorpPlace::text").extract_first()
        
        item['date'] = response.css("#lblDEventDate::text").extract_first()
        item['dateaware'] = response.css("#lblDAwareDate::text").extract_first()

        # event details

        item['relevanteventdetails'] = {
            'Position 1': {
                'Position': response.css("#lblDEvtPosition::text").extract_first(),
                'Event code': response.css("#lblDEvtReason::text").extract_first(),
                'Code before relevant event': response.css("#lblDEvtCapBefore::text").extract_first(),
                'Code after relevant event': response.css("#lblDEvtCapAfter::text").extract_first(),
                'Number of shares': response.css("#lblDEvtShare::text").extract_first(),
                'Amount of debentures': response.css("#lblDEvtAmount::text").extract_first(),
                'Currency': response.css("#lblDEvtCurrency::text").extract_first(),
                'Unit size': response.css("#lblDEvtUnitSize::text").extract_first(),                
                'Highest price on exchange': response.css("#lblDEvtHPrice::text").extract_first(),
                'Average price on exchange': response.css("#lblDEvtAPrice::text").extract_first(),
                'Average consideration off exchange': response.css("#lblDEvtAConsider::text").extract_first(),
                'Consideration code': response.css("#lblDEvtNatConsider::text").extract_first()
            },
            'Position 2': {
                'Position': response.css("#lblDEvtPosition2::text").extract_first(),
                'Event code': response.css("#lblDEvtReason2::text").extract_first(),
                'Code before relevant event': response.css("#lblDEvtCapBefore2::text").extract_first(),
                'Code after relevant event': response.css("#lblDEvtCapAfter2::text").extract_first(),
                'Number of shares': response.css("#lblDEvtShare2::text").extract_first()
            }
        }

        if response.css("#lblDBEvtAmount").extract_first() is not None:
            item['before'] = {'number': response.css("#lblDBEvtAmount").extract_first()}
            item['after'] = {'number': response.css("#lblDAEvtAmount").extract_first()}
        else:
            item['before'] = []
            for tr in response.css("#grdSh_BEvt").css("tr")[1:]:
                positionbefore = tr.css("td::text").extract()
                item['before'].append(
                    {
                        'position': positionbefore[0],
                        'number': positionbefore[1],
                        'percent': positionbefore[2]
                    }
                )

            item['after'] = []
            for tr in response.css("#grdSh_AEvt").css("tr")[1:]:
                positionafter = tr.css("td::text").extract()
                item['after'].append(
                    {
                        'position': positionafter[0],
                        'number': positionafter[1],
                        'percent': positionafter[2]
                    }
                )

        item['capacityheld'] = extractformtable('"grdCap_SS"', True)

        # further information

        item['derivativeinterests'] = extractformtable('"grdDer_SS"', True)

        item['dependentinformation'] = extractformtable('"grdFI_Sh"', True)

        item['othercorporationinterests'] = extractformtable('"grdCtrlCorp"', True)

        item['jointinterests'] = extractformtable('"grdJI_Sh"', True)

        item['trustinterests'] = extractformtable('"grdTrust_Sh"', True)

        item['s317info'] = extractformtable('"grdPA_Sh"', False)

        item['s317total'] = response.css("#lblDPATotalShare::text").extract_first()

        item['accordancepersons'] = extractformtable('"grdPer_CorpRel"', True)

        item['debenturerights'] = extractformtable('"grdGRDir_Db"', True)

        # final details
        
        item['dateformfilled'] = response.css("#lblDSignDate::text").extract_first()

        item['numberofattachments'] = response.css("#lblDNoAttachment::text").extract_first()
        
        yield item
