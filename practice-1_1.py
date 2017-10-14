#!/usr/bin/python3
#
import requests

URL = "http://sample.scraping-book.com/dp"

r = requests.get(URL)
r.encoding = "utf-8"
print(r.text)

