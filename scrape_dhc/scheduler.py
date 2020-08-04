import schedule
import time
import os
#from scrape_dhc.scrape_dhc.spiders.dhc_spider import DhcSpider

def scrape():
    os.system("scrapy crawl dhc")
    print("IMPLEMENTATION")

schedule.every().hour.do(scrape)

while 1:
    schedule.run_pending()
    time.sleep(1)