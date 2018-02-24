# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem


class NeituiSpider(scrapy.Spider):
    name = 'neitui'
    allowed_domains = ['www.neitui.me']
    start_urls = ['http://www.neitui.me']
    positionUrl = 'http://www.neitui.me/?name=job&handle=lists'
    curPage = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('ul.list-items > li')
        if (len(job_list) > 0):
            print("neitui Nums:" + str(len(job_list)))
            for job in job_list:
                item = WwwJobComItem()
                job_primary = job.css('div.positionleft > div')
                item['position_id'] = job_primary[0].css('a::attr(href)').extract_first().strip().replace("/j/", "")
                item["position_name"] = job_primary[0].css('a::text').extract_first().strip()
                item['time'] = job_primary[0].css('span::text').extract_first().strip()
                item["salary"] = job_primary[1].css('span.mr10::text').extract_first().strip().replace("k", "K")
                salary = item["salary"].split("-")
                item["avg_salary"] = (int(salary[0].replace("K", "")) + int(salary[1].replace("K", ""))) / 2
                info_primary = job_primary[1].css('span::text').extract()
                item['city'] = info_primary[5].strip()
                item['work_year'] = info_primary[1].strip()
                item['education'] = info_primary[3].strip()
                item['company_name'] = job_primary[2].css('span >a::text').extract_first().strip()
                item['finance_stage'] = job_primary[2].css('span::text').extract()[1].strip()
                item['industry_field'] = ""
                item['company_size'] = ""
                item['position_lables'] = ""
                item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['platform'] = "neitui"
                yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        self.positionUrl += "&keyword=PHP&city=%E9%83%91%E5%B7%9E&page=" + str(self.curPage)
        print("neitui page:" + str(self.curPage))
        time.sleep(0)
        return scrapy.http.FormRequest(
            self.positionUrl,
            headers=self.headers,
            callback=self.parse)
