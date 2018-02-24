# -*- coding: utf-8 -*-
import scrapy
import time
from www_job_com.items import WwwJobComItem


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/']
    positionUrl = 'https://www.zhipin.com/c101180100-p100103/h_101180100/?query='
    curPage = 0
    headers = {}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('div.job-list > ul > li')
        if (len(job_list) > 0):
            print("zhipin Nums:" + str(len(job_list)))
            for job in job_list:
                item = WwwJobComItem()
                job_primary = job.css('div.job-primary')
                item['position_id'] = job.css('div.info-primary > h3 > a::attr(data-jobid)').extract_first().strip()
                item["position_name"] = job_primary.css('div.info-primary > h3 > a > div::text').extract_first().strip()
                item["salary"] = job_primary.css('div.info-primary > h3 > a > span::text').extract_first().strip()
                salary = item["salary"].split("-")
                item["avg_salary"] = (int(salary[0].replace("K", "")) + int(salary[1].replace("K", ""))) / 2
                info_primary = job_primary.css('div.info-primary > p::text').extract()
                item['city'] = info_primary[0].strip()
                item['work_year'] = info_primary[1].strip()
                item['education'] = info_primary[2].strip()
                item['company_name'] = job_primary.css(
                    'div.info-company > div.company-text > h3 > a::text').extract_first().strip()
                company_infos = job_primary.css('div.info-company > div.company-text > p::text').extract()
                if len(company_infos) == 3:
                    item['industry_field'] = company_infos[0].strip()
                    item['finance_stage'] = company_infos[1].strip()
                    item['company_size'] = company_infos[2].strip()
                else:
                    item['industry_field'] = company_infos[0].strip()
                    item['finance_stage'] = ""
                    item['company_size'] = company_infos[1].strip()

                item['position_lables'] = ""  # job_primary.css('div.info-detail > div.tags > span::text').extract()
                item['time'] = job.css('div.info-publis > p::text').extract_first().strip()
                item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['platform'] = "zhipin"
                yield item
            yield self.next_request()

    # 发送请求
    def next_request(self):
        self.curPage += 1
        print("zhipin page:" + str(self.curPage))
        time.sleep(10)
        return scrapy.http.FormRequest(
            self.positionUrl + ("&page=%d&ka=page-%d" %
                                (self.curPage, self.curPage)),
            headers=self.headers,
            callback=self.parse)
