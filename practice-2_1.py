#!/usr/bin/python3
#
import requests
import bs4


URL = "http://sample.scraping-book.com/dp"

r = requests.get(URL)
r.encoding = "utf-8"

s = bs4.BeautifulSoup(r.text, "lxml")
print(s)

