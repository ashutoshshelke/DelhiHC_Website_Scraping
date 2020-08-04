import scrapy
import re
from ..items import ScrapeDhcItem
from scrapy.loader import ItemLoader

class DhcSpider(scrapy.Spider):
    name = "dhc"
    start_urls = [
        "http://delhihighcourt.nic.in/case.asp"
    ]

    def parse(self, response):
        next_page = response.css(".case-type-form::attr(action)").extract_first()
        yield response.follow(next_page, callback=self.start_scraping)

    def start_scraping(self, response):
        items = ScrapeDhcItem()

        for row in range(1,9):
            srno = response.xpath('//*[@id="InnerPageContent"]/ul/li[' + str(row) + ']/span[1]/text()').extract_first().strip()
            diaryno = response.xpath('//*[@id="InnerPageContent"]/ul/li['+ str(row) +']/span[2]/text()').extract_first().strip()
            status = response.xpath('//*[@id="InnerPageContent"]/ul/li['+ str(row) +']/span[2]/font/text()').extract_first().strip()
            petitioner_vs_respondent = f'''{response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()').extract_first().strip()} \n {response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()[2]').extract_first().strip()} \n {response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()[3]').extract_first().strip()}'''
            listing_date = response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[4]/text()').extract_first().strip()

            listing_date = re.sub('(\t)*(\n)*(\r)*(\xa0)*','',listing_date)
            petitioner_vs_respondent = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', petitioner_vs_respondent)
            diaryno = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', diaryno)

            items['srno'] = srno
            items['diaryno'] = diaryno
            items['status'] = status
            items['petitioner_vs_respondent'] = petitioner_vs_respondent
            items['listing_date'] = listing_date

            yield items

        # link = "http://delhihighcourt.nic.in/dhc_case_status_oj_list.asp?pno=987478"
        # yield response.follow(link, callback = self.parse)