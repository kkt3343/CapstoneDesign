import threading
import time
import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request

import encar_crawler
import KB_crawler
import kcar_crawler
import bobae_crawler

# IP주소 적기
hostip = ''
runtime = 60

encar = threading.Thread(target=encar_crawler.start_crawling, args=(hostip, runtime))
kb = threading.Thread(target=KB_crawler.start_crawling, args=(hostip, runtime))
kcar = threading.Thread(target=kcar_crawler.start_crawling, args=(hostip, runtime))
bobae = threading.Thread(target=bobae_crawler.start_crawling, args=(hostip, runtime))

try:
     encar.start()
     encar.join()
except:
     print("err")

try:
    kb.start()
    kb.join()
except:
     print("err")

try:
    kcar.start()
    kcar.join()
except:
     print("err")

try:
    bobae.start()
    bobae.join()
except:
     print("err")





