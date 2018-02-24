# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem


class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['search.51job.com']
    start_urls = ['http://search.51job.com/']
    positionUrl = ''
    curPage = 0
    headers = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('div.dw_table > div.el')
        if (len(job_list) > 1):
            print("51job Nums:" + str(len(job_list)))
            for job in job_list:
                item = WwwJobComItem()
                str_time = job.css('span.t5::text').extract_first().strip()
                if (str_time == "发布时间"):
                    continue
                else:
                    item['position_id'] = job.css('p.t1 > input::attr(value)').extract_first().strip()
                    item["position_name"] = job.css('p.t1 > span > a::text').extract_first().strip()
                    salary = job.css('span.t4::text').extract_first().strip()
                    if (salary.find("万/月") > -1):
                        salary = salary.replace("万/月", "").split("-")
                        item["salary"] = str(float(salary[0]) * 10) + "K-" + str(float(salary[1]) * 10) + "K"
                        item["avg_salary"] = (float(salary[0]) * 10 + float(salary[1]) * 10) / 2
                    elif (salary.find("万/年") > -1):
                        salary = salary.replace("万/年", "").split("-")
                        item["salary"] = str(float(salary[0]) / 12) + "K-" + str(float(salary[1]) / 12) + "K"
                        item["avg_salary"] = (float(salary[0]) / 12 + float(salary[1]) / 12) / 2
                    elif (salary.find("元/天") > -1):
                        continue
                    else:
                        salary = salary.replace("千/月", "").split("-")
                        item["salary"] = salary[0] + "K-" + salary[1] + "K"
                        item["avg_salary"] = (float(salary[0]) + float(salary[1])) / 2
                    item['city'] = job.css('span.t3::text').extract_first().strip()
                    item['work_year'] = ""
                    item['education'] = ""
                    item['company_name'] = job.css('span.t2 > a::text').extract_first().strip()

                    item['industry_field'] = ""
                    item['finance_stage'] = ""
                    item['company_size'] = ""
                    item['position_lables'] = ""
                    item['time'] = str_time
                    item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['platform'] = "51job"
                    yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        self.positionUrl = "http://search.51job.com/list/170200,000000,0000,00,9,99,php,2," + str(
            self.curPage) + ".html"
        print("51job page:" + str(self.curPage))
        time.sleep(10)
        return scrapy.http.FormRequest(self.positionUrl,
                                       headers=self.headers,
                                       callback=self.parse)
