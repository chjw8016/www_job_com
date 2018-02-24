# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem
import math


class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['zz.ganji.com']
    start_urls = ['http://zz.ganji.com/']
    positionUrl = ''
    curPage = 0
    headers = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('div.job-parttime > dl')
        if (len(job_list) > 0):
            print("ganji Nums:" + str(len(job_list)))
            for job in job_list:
                item = WwwJobComItem()
                item['position_id'] = job.css('dt > div > input::attr(value)').extract_first().strip().split(",")[0]
                item["position_name"] = "php开发工程师"
                salary = job.css('em.unit::text').extract_first().strip()
                if (salary == "面议"):
                    item["salary"] = "面议"
                    item["avg_salary"] = 0
                else:
                    salary = job.css('dt > div > p > em.lipay > i > strong::text').extract_first().strip().split("-")
                    item["salary"] = str(math.ceil(int(salary[0]) / 1000)) + "K-" + str(
                        math.ceil(int(salary[1]) / 1000)) + "K"
                    item["avg_salary"] = (int(salary[0]) + int(salary[1])) / 2000
                item['city'] = job.css('dt > div > p.site > a::text').extract_first().strip().replace("地址：", "")
                item['work_year'] = job.css('dt > div > p > em.liexp::text').extract_first().strip().replace("经验：",
                                                                                                             "")
                item['education'] = ""
                item['company_name'] = job.css('div.j-comp > a::text').extract_first().strip()
                item['industry_field'] = ""
                item['finance_stage'] = ""
                item['company_size'] = ""
                item['position_lables'] = ""
                item['time'] = job.css('p.time::text').extract_first().strip()
                item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['platform'] = "ganji"
                yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        num = (self.curPage - 1) * 32
        self.positionUrl = 'http://zz.ganji.com/zhaopin/s/f' + str(num) + '/_php/'
        print("ganji page:" + str(self.curPage))
        time.sleep(10)
        return scrapy.http.FormRequest(
            self.positionUrl,
            headers=self.headers,
            callback=self.parse)
