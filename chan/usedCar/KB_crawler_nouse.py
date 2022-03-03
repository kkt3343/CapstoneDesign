import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from KB_crawling import diagnosed_item
from KB_crawling import normal_item


def giveData(url, conn, cur, driver, isNormalItem):
    # 일반매물
    if isNormalItem:
        normal_item(url, conn, cur, driver)
    else:  # 진단매물
        diagnosed_item(url, conn, cur, driver)

    driver.close()


def start_crawling(hostip, ):
    conn = pymysql.connect(host=hostip, port=3306, user='dbAdmin', password='xoduqrb', db='usedcardb', charset='utf8')
    cur = conn.cursor()

    driver = webdriver.Chrome("WebDriver/chromedriver")
    homepage = "https://www.kbchachacha.com/"
    driver.get(homepage)
    time.sleep(2)

    # 시작페이지와 끝 페이지 정하기
    startnum = 1
    endnum = 3

    page = "https://www.kbchachacha.com/public/search/main.kbc#!?countryOrder=1&page=_PAGENUM_&sort=-orderDate"

    tmp = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div[3]/div[4]/div[2]/div[_NUM_]/div[1]/a'
    badgexpath = '//*[@id="content"]/div[2]/div/div[2]/div[2]/div[3]/div[4]/div[2]/div[_NUM_]/div[1]/span'

    for j in range(startnum, endnum):
        driver.get(page.replace("_PAGENUM_", str(j)))
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        print("============================")

        for i in range(1, 21):
            item = driver.find_element_by_xpath(tmp.replace("_NUM_", str(i))).get_attribute('href')
            print(item)

            try:
                driver.find_element_by_xpath(badgexpath.replace("_NUM_", str(i)))
                isNormalItem = False
            except:
                isNormalItem = True

            # 페이지를 열었다가 닫기

            driver.execute_script('window.open("{0}");'.format(item))
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])

            # DB에 데이터 저장하기
            giveData(item, conn, cur, driver, isNormalItem)

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)

    driver.close()
    conn.close()
