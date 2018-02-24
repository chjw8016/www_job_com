# -*- coding: utf-8 -*-
import scrapy
import time
import json
from www_job_com.items import WwwJobComItem
import math


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    curPage = 1
    city_name = "郑州"
    job_name = "PHP"
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=郑州&needAddtionalResult=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        "Referer": "https://www.lagou.com/jobs/list_php?cl=false&fromSearch=true&labelWords=&suginput=&city=郑州"}

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        try:
            html = json.loads(response.body)
        except ValueError:
            print(response.body)
            yield self.next_request()

        if (html.get("success")):
            if html.get('content').get('positionResult').get('resultSize') != 0:
                results = html.get('content').get('positionResult').get('result')
                print('lagou Nums:' + str(len(results)))
                for result in results:
                    item = WwwJobComItem()
                    item['salary'] = result.get('salary').replace("k", "K")
                    salary = item["salary"].split("-")
                    item["avg_salary"] = (int(salary[0].replace("K", "")) + int(salary[1].replace("K", ""))) / 2
                    item['city'] = result.get('city')
                    item['finance_stage'] = result.get('financeStage')
                    item['industry_field'] = result.get('industryField')
                    item['position_lables'] = result.get('positionAdvantage')
                    item['position_id'] = result.get('positionId')
                    item['company_size'] = result.get('companySize')
                    item['position_name'] = result.get('positionName')
                    item['work_year'] = result.get('workYear')
                    item['education'] = result.get('education')
                    item['company_name'] = result.get('companyShortName')
                    item['time'] = result.get("formatCreateTime")
                    item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['platform'] = "lagou"
                    yield item
                totalPage = math.floor(int(html.get('content').get('positionResult').get("totalCount")) / int(
                    html.get('content').get("pageSize")))
                self.curPage = self.curPage + 1
                if (self.curPage <= totalPage):
                    yield self.next_request()
        else:
            time.sleep(60)
            yield self.next_request()

    def next_request(self):
        print("lagou page:" + str(self.curPage))
        return scrapy.FormRequest(url=self.url, formdata={'pn': str(self.curPage), 'kd': self.job_name},
                                  method='POST',
                                  headers=self.headers, meta={'page': self.curPage, 'kd': self.job_name},
                                  dont_filter=True)
