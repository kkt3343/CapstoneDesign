import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from encar_crawling import diagnosed_item
from encar_crawling import normal_item

def giveData(url, conn, cur, driver):

    vt_index = url.find('view_type')
    if url[vt_index + 10] == 'n':
        normal_item(url, conn, cur, driver)
    else:
        diagnosed_item(url, conn, cur, driver)

    driver.close()

def start_crawling(hostip, runtime, startnum, endnum):
    start_time = time.time()
    conn = pymysql.connect(host=hostip, port=3306, user='dbAdmin', password='xoduqrb', db='usedcardb', charset='utf8')
    cur = conn.cursor()

    driver = webdriver.Chrome("WebDriver/chromedriver")
    homepage = "http://www.encar.com"
    driver.get(homepage)
    time.sleep(2)

    page = "http://www.encar.com/dc/dc_carsearchlist.do?carType=kor"
    driver.get(page)
    time.sleep(2)

    tmp = '//*[@id="sr_normal"]/tr[num]'
    tmp2 = '//*[@id="sr_normal"]/tr[num]/td[1]/div/a'

    link = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.Y.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A_PAGENUM_%2C%22limit%22%3A20%7D'

    # 시작페이지와 끝 페이지 정하기
    #startnum = 1
    #endnum = 10

    isBreaked = False
    for j in range(startnum, endnum):
        driver.get(link.replace("_PAGENUM_", str(j)))
        time.sleep(2)
        for i in range(1, 22):
            item = driver.find_element_by_xpath(tmp.replace("num", str(i)))
            # 만약 display가 none일 경우 더미데이터 이기 때문에 제외해야한다.
            if item.value_of_css_property('display') != 'none':
                item_url = driver.find_element_by_xpath(tmp2.replace("num", str(i))).get_attribute('href')

                # 주소창 출력
                print(item_url)
                driver.implicitly_wait(10)
                time.sleep(2)

                driver.execute_script('window.open("{0}");'.format(item_url))
                driver.implicitly_wait(10)
                time.sleep(2)

                driver.switch_to.window(driver.window_handles[1])

                try:
                    giveData(item_url, conn, cur, driver)
                except:
                    print("에러 발생 다음 매물을 검색합니다.")
                    driver.close()

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
