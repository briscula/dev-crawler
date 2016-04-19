# -*- coding: utf-8 -*-
# @author: zhangliangliang

import scrapy.cmdline

import re

from avarsha_spider import AvarshaSpider


_spider_name = 'ebay'

class EbaySpider(AvarshaSpider):
    name = _spider_name
    allowed_domains = ["ebay.com"]

    def __init__(self, *args, **kwargs):
        super(EbaySpider, self).__init__(*args, **kwargs)

    def find_items_from_list_page(self, sel, item_urls):
        """parse items in category page"""
        base_url = ''
        items_xpath = '//div[@class="gvtitle"]/h3/a/@href'

        # don't need to change this line
        return self._find_items_from_list_page(
            sel, base_url, items_xpath, item_urls)

    def find_nexts_from_list_page(self, sel, list_urls):
        """find next pages in category url"""
        base_url = ''
        nexts_xpath = '//td[@class="pages"]//a//@href'

        # don't need to change this line
        return self._find_nexts_from_list_page(
            sel, base_url, nexts_xpath, list_urls)

    def _extract_url(self, sel, item):
        item['url'] = sel.response.url

    def _extract_title(self, sel, item):
        title_xpath = '//*[@id="itemTitle"]/text()'
        data = sel.xpath(title_xpath).extract()
        if len(data) != 0:
            item['title'] = ' '.join(data)

    def _extract_store_name(self, sel, item):
        item['store_name'] = 'Ebay'

    def _extract_brand_name(self, sel, item):
        brand_xpath = '//h2[@itemprop="brand"]/span/text()'
        data = sel.xpath(brand_xpath).extract()
        if len(data) != 0:
            item['brand_name'] = data[0]
        else:
            item['brand_name'] = 'Ebay'

    def _extract_sku(self, sel, item):
        sku_xpath = '//a[contains(@data-itemid, "")]/@data-itemid'
        data = sel.xpath(sku_xpath).extract()
        if len(data) != 0:
            item['sku'] = data[0]

    def _extract_features(self, sel, item):
        pass

    def _extract_description(self, sel, item):
        description_xpath = '//span[@id="vi-cond-addl-info"]/text()'
        data = sel.xpath(description_xpath).extract()
        if len(data) != 0:
            item['description'] = data[0]

    def _extract_size_chart(self, sel, item):
        pass

    def _extract_color_chart(self, sel, item):
        pass

    def _extract_image_urls(self, sel, item):
        imgs = []
        for line in sel.response.body.split(','):
            idx1 = line.find('maxImageUrl\":\"')
            if idx1 != -1:
                idx2 = line.find('?', idx1)
                img_urlT = line[idx1 + \
                    len('maxImageUrl\":\"'):idx2].strip()
                img_url = img_urlT.replace('\u002F', '/')
                imgs.append(img_url)
            item['image_urls'] = imgs

    def _extract_colors(self, sel, item):
        colors_xpath = '//select[@name="Color"]//option/text()'
        data = sel.xpath(colors_xpath).extract()
        if len(data) != 0:
            item['colors'] = data[1:]

    def _extract_sizes(self, sel, item):
        sizes_xpath = '//select[@name="Size"]//option/text()'
        data = sel.xpath(sizes_xpath).extract()
        if len(data) != 0:
            item['sizes'] = data[1:]

    def _extract_stocks(self, sel, item):
        pass

    def extract_price_num(self, str_pri):
        pattern = re.compile(r'\d+\.?\d+')
        match = re.search(pattern, str_pri)
        return str(match.group())

    def _extract_price(self, sel, item):
        price_xpath = '//span[@itemprop="price"]/text()'
        sale_price_xpath = '//span[@id="mm-saleDscPrc"]/text()'
        data = sel.xpath(price_xpath).extract()
        if len(data) != 0:
            price_number = self.extract_price_num(data[0])
            item['price'] = self._format_price('USD', price_number)
        else:
            data = sel.xpath(sale_price_xpath).extract()
            if len(data) != 0:
                price_number = self.extract_price_num(data[0])
                item['price'] = self._format_price('USD', price_number)

    def _extract_list_price(self, sel, item):
        list_price_xpath = '//span[@id="mm-saleOrgPrc"]/text()'
        data = sel.xpath(list_price_xpath).extract()
        if len(data) != 0:
            price_number = self.extract_price_num(data[0])
            item['list_price'] = self._format_price('USD', price_number)

    def _extract_low_price(self, sel, item):
        pass

    def _extract_high_price(self, sel, item):
        pass

    def _extract_is_free_shipping(self, sel, item):
        pass

    def _extract_review_count(self, sel, item):
        pass

    def _extract_review_rating(self, sel, item):
        pass

    def _extract_best_review_rating(self, sel, item):
        pass

    def _extract_review_list(self, sel, item):
        pass

def main():
    scrapy.cmdline.execute(argv = ['scrapy', 'crawl', _spider_name])

if __name__ == '__main__':
    main()
