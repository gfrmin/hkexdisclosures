import re
import scrapy.dupefilters
from scrapy.utils.request import request_fingerprint

class FormIDFilter(scrapy.dupefilters.RFPDupeFilter):
    def request_fingerprint(self, request):
        formidre = re.search(r'(NSForm.+\.aspx\?fn=.+?)&', request.url)
        if formidre:
            fingerprint = formidre.group(1)
        else:
            fingerprint = request_fingerprint(request)
        return fingerprint
