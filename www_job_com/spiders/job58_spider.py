# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem
import math


class Job58Spider(scrapy.Spider):
    name = 'job58'
    allowed_domains = ['zz.58.com']
    start_urls = ['http://zz.58.com/']
    positionUrl = 'http://zz.58.com/job/?key=php&final=1&jump=1'
    curPage = 0
    headers = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('li.job_item')
        if (len(job_list) > 0):
            print("job58 Nums:" + str(len(job_list)))
            for job in job_list:
                item = WwwJobComItem()
                item['time'] = job.css('span.sign::text').extract_first().strip()
                if (item['time'] == "优选" or item['time'] == "精准"):
                    continue
                else:
                    item['position_id'] = job.css('div.job_name > a::attr(urlparams)').extract_first().strip().replace(
                        "psid=", "").replace("&entinfo=", "").replace("_p", "").replace("_j", "")
                    item[
                        "position_name"] = job.css('div.job_comp > p.job_require >span::text').extract()[
                        0].strip()
                    salary = job.css('p.job_salary::text').extract_first().strip()
                    if (salary == "面议"):
                        new_salary = salary
                        item["avg_salary"] = 0
                    elif (salary == "1000"):
                        new_salary = "1K"
                        item["avg_salary"] = 1.0
                    else:
                        salary = salary.split("-")
                        new_salary = str(math.ceil(int(salary[0]) / 1000)) + "K-" + str(
                            math.ceil(int(salary[1]) / 1000)) + "K"
                        item["avg_salary"] = (int(salary[0]) + int(salary[1])) / 2000
                    item["salary"] = new_salary
                    item['city'] = "郑州"
                    item['work_year'] = job.css("div.job_comp > p.job_require > span::text").extract()[2].strip()
                    item['education'] = job.css("div.job_comp > p.job_require > span::text").extract()[1].strip()
                    item['company_name'] = job.css('div.comp_name > a::text').extract_first().strip()

                    item['industry_field'] = ""
                    item['finance_stage'] = ""
                    item['company_size'] = ""
                    label = job.css("div.job_wel > span::text").extract()
                    item['position_lables'] = ",".join(label)
                    item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['platform'] = "job58"
                    yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        if (self.curPage > 1):
            self.positionUrl = "http://zz.58.com/job/pn" + str(self.curPage) + "/?key=php&final=1&jump=1"
        print("job58 page:" + str(self.curPage))
        time.sleep(10)
        return scrapy.http.FormRequest(
            self.positionUrl,
            headers=self.headers,
            callback=self.parse)
