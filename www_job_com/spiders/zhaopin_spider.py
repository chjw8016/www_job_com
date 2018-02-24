# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['sou.zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/']
    positionUrl = ''
    curPage = 0
    headers = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('table.newlist > tr')
        if (len(job_list) > 1):
            print("zhaopin Nums:" + str(len(job_list)))
            i = 0;
            for job in job_list:
                i += 1
                if (i > 1 and (i % 2) == 0):
                    item = WwwJobComItem()
                    item['position_id'] = job.css('td.zwmc > input::attr(data-monitor)').extract_first().strip().replace("|", "")
                    name = job.css('td.zwmc > div > a').extract_first().strip()
                    if (name.find("php") > -1 or name.find("Php") > -1 or name.find("PHP") > -1):
                        item["position_name"] = "php研发工程师"
                        salary = job.css('td.zwyx::text').extract_first().strip().split("-")
                        item["salary"] = str(int(int(salary[0]) / 1000)) + "K-" + str(int(int(salary[1]) / 100)) + "K"
                        item["avg_salary"] = (int(salary[0]) + int(salary[1])) / 2000
                        item['city'] = "郑州"
                        item['work_year'] = ""
                        item['education'] = ""
                        item['company_name'] = job.css('td.gsmc > a::text').extract_first().strip()
                        item['industry_field'] = ""
                        item['finance_stage'] = ""
                        item['company_size'] = ""
                        item['position_lables'] = ""
                        item['time'] = job.css('td.gxsj > span::text').extract_first().strip()
                        item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        item['platform'] = "zhaopin"
                        yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        if (self.curPage <= 10):
            self.positionUrl = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%83%91%E5%B7%9E&kw=php&sm=0&fl=719&isadv=0&sb=1&isfilter=1&et=2&p=" + str(
                self.curPage)
            print("zhaopin page:" + str(self.curPage))
            time.sleep(10)
            return scrapy.http.FormRequest(self.positionUrl,
                                           headers=self.headers,
                                           callback=self.parse)