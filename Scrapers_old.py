import requests
import time
import excel_writer_old
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from dateutil.relativedelta import *
'''
TODO:
Excel (löst)
chatgpt (kan finslipas lite)
spara datum av reviewn (löst)
hype??? (fuck you webhallen) (löst)
vissa reviews har ingen text. spara stjärnor? (löst)
infiniscroll
olika kategorier (löst)
Använda network tabben istället https://stackoverflow.com/questions/52633697/selenium-python-how-to-capture-network-traffics-response
'''

# 'https://www.webhallen.com/se/category/3965-Laptop-Barbar-dator?page=1'
# "https://www.webhallen.com/se/section/3-Datorer-Tillbehor"
class WH_scraper:
    def __init__(self, url):
        # kan iterera över sektion men blir så jävla mycket
        self.now = datetime.now()
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.writer = excel_writer_old.Scraping_writer(r"C:\Users\Gustav\Desktop\företag\review_data2.xlsx")


    def scrape_site(self):
        try:
            [category_names, category_urls] = self.get_categories()
            print("Categories Recieved")
            for [category_name, category_url] in zip(category_names, category_urls):
                self.scrape_category(category_name, category_url)
        except KeyboardInterrupt:
            self.close_driver()

    def get_categories(self):
        self.driver.get(self.url)
        time.sleep(3)
        self.cookiebutton()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        category_tiles = soup.select("#main-container > article > div.parent-section > div:nth-child(23) > div > ul > li > a")
        category_urls = ["https://www.webhallen.com" + category_tile["href"] for category_tile in category_tiles]
        category_names = [category_tile.get_text(strip = True) for category_tile in category_tiles]
        return [category_names, category_urls]
    
    def cookiebutton(self):
        try:
            # click cookie button
            self.driver.find_element(By.CSS_SELECTOR, "#cookie-banner > div > button:nth-child(1)").click()
        except:
            pass

    def scrape_category(self, category_name, category_url):
        self.writer.set_sheet(category_name)
        [product_names, product_urls] = self.get_products_in_category(category_url)
        print("Recieved products in category")
        reviews = []
        for product_name, product_url in zip(product_names, product_urls):
            [reviews_text, review_dates, total_stars, review_stars] = self.scrape_product(product_url)
            self.writer.write_data(product_url, product_name, reviews_text, review_dates, total_stars, review_stars) 
            print("Writing product")

    def get_products_in_category(self, url):
        self.driver.get(url)
        time.sleep(1) # bör justeras
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # "#main-container > article > div.product-browser > div.mt-4 > div:nth-child(1) > div > div > div.panel-top > a"
        panels = soup.select("#main-container > article > div.product-browser > div.mt-4 > div > div > div > div.panel-top > a", href=True)
        product_urls = []
        product_names = []
        for panel in panels:
            product_names.append(panel["title"])
            product_urls.append("https://www.webhallen.com" + panel["href"])
        return [product_names, product_urls]
    
    def close_driver(self):
        self.driver.close()   

    def scrape_product(self, url):
        self.driver.get(url)
        time.sleep(0.5)
        reviews_text = []
        review_stars = []
        review_dates = []
        total_stars = ""

        try:
            all_reviews_button = self.driver.find_element(By.CSS_SELECTOR, "#p-reviews > div:nth-child(3) > center > a")
            self.driver.execute_script("arguments[0].scrollIntoView();", all_reviews_button)
            all_reviews_button.click()
        except:
            # expanding reviews not necessarry
            pass

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        reviews_html = soup.find_all(class_="review")
        if reviews_html == []:
            # No reviews
            # will return [[],"",[]]
            return [reviews_text, review_dates, total_stars, review_stars]

        # Could potentially cause issues. Only works as intended if the first stars
        # are the total. If no reviews exist, this fetches stars from suggested products.
        total_stars = soup.select_one(".stars")["title"]        
        for review_html in reviews_html:
            if review_html.find(class_="flames") is None:
                # Hype reviews. Varför webhallen? Varför?
                try:
                    reviews_text.append(review_html.find(class_="review-text").get_text())
                except AttributeError:
                    # No text in review, only stars
                    reviews_text.append("")
                review_stars.append(review_html.find(class_="stars")["title"])
                print(review_html.find(class_="sub-title").get_text(strip = True))
                review_dates.append(self.date_handler(review_html.find(class_="sub-title").get_text(strip = True)))

        # Har med massor av newline och skit. Dåligt? Vet inte om chatgpt fattar kontexten.
        return [reviews_text, review_dates, total_stars, review_stars]
    
    def close(self):
        self.writer.close()
        self.driver.quit()
    
    def date_handler(self, date_string):
        
        date_split = date_string.split(" ")
        text_to_int = {"ett": 1,
                       "en":1,
                       "två":2,
                       "tre":3,
                       "fyra":4,
                       "fem":5,
                       "sex":6,
                       "sju":7,
                       "åtta":8,
                       "nio":9,
                       "tio":10,
                       "elva":11,
                       "tolv":12
                        }
        if date_split[0] == "ungefär":
            date_split.pop(0)
        
        try: 
            date_split[0] = int(date_split[0])
        except:
            date_split[0] = text_to_int[date_split[0]]

        time_amount = date_split[0]

        if date_split[1] == "år":
            delta = relativedelta(years=time_amount)
        elif date_split[1] == "månader":
            delta = relativedelta(months=time_amount)
        elif date_split[1] == "dagar":
            delta = relativedelta(days=time_amount)
        elif date_split[1] == "minuter":
            delta = relativedelta(minutes=time_amount)
        elif date_split[1] == "sekunder":
            delta = relativedelta(seconds=time_amount)
        return (self.now - delta).date()
        


        

    
