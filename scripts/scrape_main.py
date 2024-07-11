import Scrapers
# "https://www.webhallen.com/se/section/3-Datorer-Tillbehor"
# 'https://www.webhallen.com/se/category/3965-Laptop-Barbar-dator?page=1'
def scrape_webhallen():
    wh_scraper = Scrapers.WH_scraper("https://www.webhallen.com/se/section/3-Datorer-Tillbehor", r"C:\Users\Gustav\Desktop\företag\review_data3.xlsx")
    wh_scraper.scrape_site()
    wh_scraper.close()

scrape_webhallen()
