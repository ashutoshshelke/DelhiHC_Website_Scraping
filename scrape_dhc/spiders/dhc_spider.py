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
        #using first method search all cases
        #next_page stores the address of next page
        next_page = response.css(".case-type-form::attr(action)").extract_first()
        yield response.follow(next_page, callback=self.start_scraping)

    def start_scraping(self, response):
        items = ScrapeDhcItem()

        #scrape data from current page
        for row in range(1,9):

            try:
                srno = response.xpath('//*[@id="InnerPageContent"]/ul/li[' + str(row) + ']/span[1]/text()').extract_first().strip()
                diaryno = response.xpath('//*[@id="InnerPageContent"]/ul/li['+ str(row) +']/span[2]/text()').extract_first().strip()
                status = response.xpath('//*[@id="InnerPageContent"]/ul/li['+ str(row) +']/span[2]/font/text()').extract_first().strip()
                petitioner_vs_respondent = f'''{response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()').extract_first().strip()} \n {response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()[2]').extract_first().strip()} \n {response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[3]/text()[3]').extract_first().strip()}'''
                listing_date = response.xpath('//*[@id="InnerPageContent"]/ul/li['+str(row)+']/span[4]/text()').extract_first().strip()

            except:
                continue

            listing_date = re.sub('(\t)*(\n)*(\r)*(\xa0)*','',listing_date)
            srno = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', srno)
            status = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', status)
            petitioner_vs_respondent = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', petitioner_vs_respondent)
            diaryno = re.sub('(\t)*(\n)*(\r)*(\xa0)*', '', diaryno)

            items['srno'] = srno
            #items['_id'] = srno
            items['diaryno'] = diaryno
            items['status'] = status
            items['petitioner_vs_respondent'] = petitioner_vs_respondent
            items['listing_date'] = listing_date

            yield items

        #goto next page (scrape 5 pages only)
        for a in response.css('#InnerPageContent a::attr(href)')[:5]:
            print("in last for")
            yield response.follow(a, callback= self.start_scraping)
