import json
import requests
from datetime import tzinfo, timedelta, datetime
import re
from Scrapers import WH_scraper
# site = requests.get("https://www.webhallen.com/api/productdiscovery/category/3965?page=1").json()
# # print(site)
# print(re.findall("\d+", "/category/16090-Datortillbehor"))
# ungefär en månad sedan
temp = WH_scraper("bleh")
print(temp.date_handler("ungefär en månad sedan"))
# print(site["products"])
# for product in site["products"]:
#     print(product["id"])
#     print(product["name"])
# print(json.dumps(site, indent=4))