import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from dateutil.relativedelta import *
import re
from abc import ABC, abstractmethod

import Excel_Writer

'''
TODO:
Excel (löst)
chatgpt (kan finslipas lite)
spara datum av reviewn (löst)
hype??? (varför webhallen) (löst)
vissa reviews har ingen text. spara stjärnor? (löst)
infiniscroll (löst)
olika kategorier (löst)
Implementera JSON för scrape_product i webhallen. Group syftar på olika varianter av en produkt. Typ färger på en macbook.
'''


class Review_Scraper(ABC):
    def __init__(self, url: str, output_file: str, products_url: str = "", categories_url: str = "") -> None:
        self.writer = Excel_Writer.Scraping_writer(output_file)
        self.driver = webdriver.Chrome()
        self.url = url
    
    def scrape_site(self) -> None:
        try:
            category_names_ids = self.get_categories()
            for category_name_id in category_names_ids:
                self.scrape_category(category_name_id)
        except Exception as e: 
            print(e)
        self.close()

    def scrape_category(self, category_name: str, category_id: str) -> None:
        '''
        scrapes AND writes. dont like that.
        Want to seperate writing and scraping, but then I would have to write a whole category at a time.
        rip memory.
        '''
        self.writer.set_sheet(category_name)
        product_names_ids = self.get_products_in_category(category_id)
        for product_name, product_id in product_names_ids:
            [reviews_text, review_dates, review_stars] = self.scrape_product(product_id)

            product_url = self.product_id_to_url(product_id)
            self.writer.write_data([product_name], [reviews_text, review_dates, review_stars], link=product_url) 
        self.writer.save()

    @abstractmethod
    def get_products_in_category(self, category_id: str) -> list[list[str], list[str]]:
        '''
        returns: [category_names, category_ids]
        '''
        pass

    @abstractmethod
    def get_categories(self) -> list[list[str], list[str]]:
        '''
        returns: [category_names, category_ids]
        '''
        pass

    @abstractmethod
    def scrape_product(self, product_id: str) -> list[list[str], list[str], list[str]]:
        '''
        returns: [reviews_text, review_dates, review_stars]
        '''
        pass

    def product_id_to_url(self, product_id: str) -> str:
        return self.products_url + product_id
    
    def category_id_to_url(self, category_id: str) -> str:
        return self.categories_url + category_id

    def close(self) -> None:
        self.writer.close()
        self.driver.quit()


class WH_scraper(Review_Scraper):
    def __init__(self, url: str, output_file: str) -> None:
        # kan iterera över sektion men blir så jävla mycket
        super().__init__(url, output_file, "https://www.webhallen.com/se/product/", "https://www.webhallen.com/api/productdiscovery/category/")
        self.now = datetime.now()
        self.driver.implicitly_wait(1)

    def get_categories(self) -> list[list[str], list[str]]:
        self.driver.get(self.url)
        time.sleep(3)
        self.cookiebutton()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        category_tiles = soup.select("#main-container > article > div.parent-section > div:nth-child(23) > div > ul > li > a")
        category_ids = [str(re.findall(r"\d+", category_tile["href"]))[0] for category_tile in category_tiles] # extract id with regex. findall gives list with one element.
        category_names = [category_tile.get_text(strip = True) for category_tile in category_tiles]
        return [category_names, category_ids]

    def get_products_in_category(self, category_id: str) -> list[list[str], list[str]]:
        page = 1
        product_ids = []
        product_names = []
        while True:
            site = requests.get(self.category_id_to_url(category_id)+"?page="+str(page)).json()
            if site["products"] == []:
                break
            for product in site["products"]:
                product_ids.append(str(product["id"]))
                product_names.append(str(product["name"]))
            page +=1

        return [product_names, product_ids]
    
    def scrape_product(self, product_id: str) -> list[list[str], list[str], list[str]]:
        '''
        Could almost certainly be done with json, much, much faster.
        But it looks less cool.
        '''
        url = self.product_id_to_url(product_id)
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
            # When product has no reviews. will return [[],"",[]]
            return [reviews_text, review_dates, total_stars, review_stars]

        # Could potentially cause issues. Only works as intended if the first stars
        # are the total. If no reviews exist, this fetches stars from suggested products.
        # Otherwise this works, though I dont care for total stars anymore
        # total_stars = soup.select_one(".stars")["title"]   
        #   
        for review_html in reviews_html:
            if review_html.find(class_="flames") is None:
                # Hype reviews. Varför webhallen? Varför?
                try:
                    reviews_text.append(review_html.find(class_="review-text").get_text(strip = True))
                except AttributeError:
                    # No text in review, only stars
                    reviews_text.append("")
                review_stars.append(review_html.find(class_="stars")["title"])
                # print(review_html.find(class_="sub-title").get_text(strip = True))
                review_dates.append(self.date_handler(review_html.find(class_="sub-title").get_text(strip = True)))
        return [reviews_text, review_dates, review_stars]

    def cookiebutton(self) -> None:
        # click cookie button
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#cookie-banner > div > button:nth-child(1)").click()
        except:
            pass

    def date_handler(self, date_string: str) -> datetime:
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
        if date_split[0] == "ungefär" or date_split[0] == "över" or date_split[0] == "nästan":
            date_split.pop(0)
        try: 
            date_split[0] = int(date_split[0])
        except:
            date_split[0] = text_to_int[date_split[0]]

        time_amount = date_split[0]

        if date_split[1] == "år":
            delta = relativedelta(years=time_amount)
        elif date_split[1] == "månader" or date_split[1] == "månad":
            delta = relativedelta(months=time_amount)
        elif date_split[1] == "dagar" or date_split[1] == "dag":
            delta = relativedelta(days=time_amount)
        elif date_split[1] == "minuter" or date_split[1] == "dag":
            delta = relativedelta(minutes=time_amount)
        elif date_split[1] == "sekunder" or date_split[1] == "sekund":
            delta = relativedelta(seconds=time_amount)
        return (self.now - delta).date()
        


        

    
