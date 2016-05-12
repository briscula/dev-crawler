# -*- coding: utf-8 -*-
# author: donglongtu

import scrapy.cmdline
import re

from avarsha_spider import AvarshaSpider


_spider_name = 'email'

class EmailSpider(AvarshaSpider):
    name = _spider_name
    allowed_domains = []
    email_list = {}

    def __init__(self, *args, **kwargs):
        super(EmailSpider, self).__init__(*args, **kwargs)

    def find_nexts_from_list_page(self, sel, list_urls):
        """find next pages in category url"""

        base_url = self.start_urls[0]
        nexts_xpath = '//a[not(starts-with(@href,"mail"))]/@href'

        # don't need to change this line
        return self._find_nexts_from_list_page(
            sel, base_url, nexts_xpath, list_urls)

    def _extract_url(self, sel, item):
        item['url'] = sel.response.url

    def _extract_email_list(self, sel, item):
        item['email'] = list(set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", sel.response.body, re.I)))

def main():
    scrapy.cmdline.execute(argv = ['scrapy', 'crawl', _spider_name])

if __name__ == '__main__':
    main()