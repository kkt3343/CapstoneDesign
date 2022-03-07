import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from Notification import notify


def crawl_item(url, conn, cur, driver):
    time.sleep(2)

    site = '보배드림'
    title = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/h3').text

    gallery_data = driver.find_element_by_class_name('gallery-data')
    carnumber = gallery_data.find_element_by_tag_name('dd').text
    carnumber = carnumber.replace("차량번호 ", "")
    
    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        print('중복 매물입니다.')
        return
    
    cartype = '확인 불가'

    #제조사
    new_window = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]/a[1]').click()
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(2)
    model_text = driver.find_element_by_xpath('//*[@id="used-price"]/div[2]/div[2]/div[1]/h4').text
    manufacturer = ''
    
    searchWord = model_text.split()[0]
    if searchWord == 'GM대우' or searchWord == '쉐보레(국산)':
        searchWord = '쉐보레/대우'
    sql = 'SELECT DISTINCT manufacturer1 FROM BobaeModel WHERE manufacturer1 LIKE "%{0}%"'
    sql = sql.format(searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        manufacturer = rows[0][0]
        
    if manufacturer == '':
        print('제조사 구분 중 오류 발생')
        print(title)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        return
    
    #모델명 확인
    searchWord = model_text.replace(manufacturer, '')
    searchWord = searchWord.replace('GM대우', '').replace('쉐보레(국산)', '')
    searchWord = searchWord.strip()
    model_detail = ''

    sql = 'SELECT * FROM BobaeModel WHERE model_detail1 = "{0}"'
    sql = sql.format(searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        manufacturer = rows[0][3]
        model = rows[0][4]
        model_detail = rows[0][5]
        
    if model_detail == '':
        print('모델 구분 중 오류 발생!')
        print(title)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        return

    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    
    
    #가격
    temp = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/span/b').text.split(',')
    price = ''
    for i in temp:
        price += i
    price = int(price + '0000')

    #주행거리
    distance = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]').text
    distance = distance.replace(" km", "").replace(",", "")


    #배기량
    displacement = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]').text
    displacement = displacement.split()[0] + displacement.split()[1]
    
    # 연식
    temp = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]').text # 연식
    temp = temp[:7].split('.')
    year = temp[0][2:] + '년 '
    month = temp[1] + '월식'
    caryear = year + month # 연식
    
    carcolor = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]').text # 색상
    carfuel = driver.find_element_by_xpath('//*[@id="bobaeConent"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]').text # 연료
    
    # 사진 가져오기
    filename = carnumber

    picturexpath = '//*[@id="imgPos"]/li[1]/a/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')
    imglink = "carimg/bobae/" + filename + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    #url 모바일로 변경
    mobile_url = 'https://m.bobaedream.co.kr/mycar/mview/CARID'
    id_start = url.find('no=') + 3
    id_length = url[id_start:].find('&')
    id_end = id_start + id_length
    carid = url[id_start:id_end]
    mobile_url = mobile_url.replace('CARID', carid)
    
    # DB에 저장
    sql = 'insert into usedCar values(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", {8}, {9}, "{10}", "{11}", "{12}", "{13}", "{14}")'
    sql = sql.format(mobile_url, site, title, carnumber, cartype, manufacturer, model, model_detail, price, distance, displacement, caryear, carcolor, carfuel, imglink)
    cur.execute(sql)
    conn.commit()
    notify(conn, cur, title, model, caryear, distance, price)
