import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from bobae_crawling import crawl_item

def giveData(url, conn, cur, driver):

    crawl_item(url, conn, cur, driver)

    driver.close()

def start_crawling(hostip, runtime, startnum, endnum):
    start_time = time.time()
    conn = pymysql.connect(host=hostip, port=3306, user='dbAdmin', password='xoduqrb', db='usedcardb', charset='utf8')
    cur = conn.cursor()

    # 보배드림
    driver = webdriver.Chrome("WebDriver/chromedriver")
    homepage = "https://www.bobaedream.co.kr/"
    driver.get(homepage)
    time.sleep(2)

    # 국산차량
    page = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K"
    driver.get(page)
    time.sleep(2)

    # 매물 Xpath
    pagexpath = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K&page=__NUM__&order=S11&view_size=20"

    # 시작페이지와 끝 페이지 정하기
    #startnum = 1
    #endnum = 15

    isBreaked = False
    for i in range(startnum, endnum + 1):
        driver.get(pagexpath.replace("__NUM__", str(i)))
        time.sleep(2)
        print("페이지 :" + str(i))
        item_container = driver.find_element_by_xpath('//*[@id="listCont"]/div[1]/ul')
        item_list = item_container.find_elements_by_class_name('product-item')
        for item in item_list:
            price = item.find_element_by_class_name('mode-cell.price').text
            if price[-2:] != '만원':
                print('가격 문제로 크롤링 X')
                continue
            if int(price.replace('만원', '').replace(',', '') + '0000') >= 1000000000:
                print('가격 문제로 크롤링 X')
                continue
            item_url = item.find_element_by_tag_name('a').get_attribute('href')
            print(item_url)
            driver.implicitly_wait(10)
            time.sleep(1)

            driver.execute_script('window.open("{0}");'.format(item_url))
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])

            giveData(item_url, conn, cur, driver)

            driver.switch_to.window(driver.window_handles[0])
            driver.implicitly_wait(10)
            time.sleep(2)
            print('작동 시간 :', time.time() - start_time)
            if time.time() - start_time > runtime:
                isBreaked = True
                break
        if isBreaked:
            break

    driver.quit()
    conn.close()
