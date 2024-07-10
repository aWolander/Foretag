
import requests
from bs4 import BeautifulSoup


url = 'https://www.webhallen.com/se/product/364141-Acer-Predator-Helios-Neo-16-PHN16-71-9498-16-WQXGA-IPS-i9-13900HX-32GB-1TB-RTX4070#p-reviews'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

reviews = soup.find_all("p")
#p-reviews > div:nth-child(2) > div:nth-child(3) > div.review-text
print(reviews)
