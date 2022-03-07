import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from kcar_crawling import direct_sales
from kcar_crawling import _3d_sales

def giveData(url, conn, cur, driver, is3D):
    if not is3D:
        direct_sales(url, conn, cur, driver)
    else:
        _3d_sales(url, conn, cur, driver)

    driver.close()

def start_crawling(hostip, runtime, startnum, endnum):
    start_time = time.time()
    conn = pymysql.connect(host=hostip, port=3306, user='dbAdmin', password='xoduqrb', db='usedcardb', charset='utf8')
    cur = conn.cursor()

    driver = webdriver.Chrome("WebDriver/chromedriver")
    homepage = "https://www.kcar.com/"
    driver.get(homepage)
    time.sleep(2)

    page = "https://www.kcar.com/car/search/car_search_list.do"
    driver.get(page)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="filterSearch"]/section[1]/div[3]/ul/label[2]').click()
    time.sleep(2)

    carxpath = '//*[@id="kcarSearchList"]/li[num]'
    pageButton = '//*[@id="kcarSearchListPaging"]/div/button[bNum]'

    # 시작페이지와 끝 페이지 정하기
    #startnum = 1
    #endnum = 20

    isBreaked = False
    for i in range(startnum, endnum+1):
        print(str(i) + "페이지")
        driver.find_element_by_xpath(pageButton.replace('bNum', str((i-1) % 10 + 1))).click()
        driver.implicitly_wait(10)
        time.sleep(1)

        for j in range(1, 16):
            item = driver.find_element_by_xpath(carxpath.replace("num", str(j)))

            atag = item.find_element_by_tag_name('a')
            markvr = atag.find_elements_by_class_name('mark.vr')
            is3D = False
            if len(markvr) > 0:
                is3D = True
            else:
                is3D = False

            item_url = item.find_element_by_tag_name('a').get_attribute('href')

            print(item_url)

            driver.execute_script('window.open("{0}");'.format(item_url))
            driver.implicitly_wait(10)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])

            giveData(item_url, conn, cur, driver, is3D)

            driver.switch_to.window(driver.window_handles[0])
            driver.implicitly_wait(10)
            time.sleep(1)
            print('작동 시간 :', time.time() - start_time)
            if time.time() - start_time > runtime:
                isBreaked = True
                break
        if isBreaked:
            break

        if i % 10 == 0:
            driver.find_element_by_xpath('//*[@id="kcarSearchListPaging"]/button[2]').click()
            time.sleep(2)

    driver.quit()
    conn.close()
