#!/usr/bin/env python
# coding: utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from pic_spider.items import PicSpiderItem


class ImageSpider(CrawlSpider):
    name = "image"
    img_urls = []
    allowed_domains = [
        "mzitu.com"
    ]
    start_urls = [
        "http://www.mzitu.com/"
    ]
    rules = (
        Rule(LinkExtractor(
            allow=('http://www.mzitu.com/\d{1,6}',),
            deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')
        ),
            callback="parse_item",
            follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        item = PicSpiderItem()
        # max_num为页面最后一张图片的位置
        max_num = response.xpath(
            "descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(
            default="N/A")
        item['imgs_title'] = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        item['imgs_url'] = response.url
        for num in range(1, int(max_num)):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            yield scrapy.Request(page_url, callback=self.img_url)
        item['img_url'] = self.img_urls
        yield item

    def img_url(self, response, ):
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.img_urls.append(img_url)
