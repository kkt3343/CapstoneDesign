import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from Notification import notify

def diagnosed_item(url, conn, cur, driver): #진단 매물
    time.sleep(3)

    data = driver.find_element_by_xpath('//*[@id="carPic"]/div[1]/ul[1]').text.split('\n')
    site = '엔카'

    brand = driver.find_element_by_xpath('//*[@id="carPic"]/div[1]/div[1]/strong/span[1]').text
    detail = driver.find_element_by_xpath('//*[@id="carPic"]/div[1]/div[1]/strong/span[2]').text
    title = brand + ' ' + detail # 타이틀

    carnumber = data[7] # 차번호

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        print('중복 매물입니다.')
        return
    
    cartype = data[3] # 차종
    
##    #제조사
##    searchWord = driver.find_element_by_xpath('//*[@id="mnfcnm"]').get_attribute('value')
##    manufacturer = ''
##
##    sql = 'SELECT DISTINCT manufacturer FROM carModel WHERE manufacturer = "{0}"'
##    sql = sql.format(searchWord)
##    cur.execute(sql)
##    rows = cur.fetchall()
##    if len(rows) == 1:
##        manufacturer = rows[0][0]
##
##    if manufacturer == '':
##        print('제조사 구분 중 오류 발생')
##        print(title)
##        return
    
    #모델명 확인
    searchWord = driver.find_element_by_xpath('//*[@id="mdlnm"]').get_attribute('value')
    model_detail = ''

    sql = 'SELECT * FROM EncarModel WHERE model_detail1 = "{0}"'
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
        return
    
    #가격
    temp = driver.find_element_by_xpath('//*[@id="scrFix"]/div[1]/div/em/span').text.split(',')
    price = ''
    for i in temp:
        price += i
    price = int(price + '0000')

    distance = data[0].replace(',', '').replace('Km', '') # 주행거리
    displacement = data[4]
    
    caryear = data[1].split()[0] + ' ' + data[1].split()[1] # 연식
    carcolor = data[6]
    carfuel = data[2] # 연료
    
    # 사진 가져오기
    filename = carnumber

    picturexpath = '//*[@id="carPic"]/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')

    #img2 = driver.find_element_by_class_name('photo_b').get_attribute('src')
    imglink = "carimg/encar/" + filename + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    #url 모바일로 변경
    mobile_url = 'https://fem.encar.com/cars/detail/CARID?listAdvType=share&adnm=mo_detail_url'
    id_start = url.find('carid') + 6
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

def normal_item(url, conn, cur, driver): #일반등록 매물
    #driver.get(url)
    time.sleep(2)

    data = driver.find_element_by_xpath('//*[@id="areaBase"]/div[2]/div[1]/div[2]').text.split('\n')
    site = '엔카'

    brand = driver.find_element_by_xpath('//*[@id="areaBase"]/div[2]/div[1]/h1/span[1]').text
    detail = driver.find_element_by_xpath('//*[@id="areaBase"]/div[2]/div[1]/h1/span[2]').text
    title = brand + ' ' + detail # 타이틀

    carnumber = data[7] # 차번호

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        print('중복 매물입니다.')
        return
    
    cartype = data[3] # 차종
    
##    #제조사
##    titleList = title.split()
##    searchWord = ''
##    manufacturer = ''
##
##    for i in range(len(titleList)):
##        searchWord += titleList[i]
##        sql = 'SELECT DISTINCT manufacturer FROM carModel WHERE manufacturer = "{0}"'
##        sql = sql.format(searchWord)
##        cur.execute(sql)
##        rows = cur.fetchall()
##        if len(rows) == 1:
##            manufacturer = rows[0][0]
##            break
##        searchWord += ' '
##
##    if manufacturer == '':
##        print('제조사 구분 중 오류 발생')
##        print(title)
##        return
    
    #모델명 확인
    searchWord = driver.find_element_by_xpath('//*[@id="mdlnm"]').get_attribute('value')
    model_detail = ''

    sql = 'SELECT * FROM EncarModel WHERE model_detail1 = "{0}"'
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
        return
    
    #가격
    price = driver.find_element_by_xpath('/html/head/meta[10]').get_attribute('content')
    price = int(price + '0000')

    distance = data[0].replace(',', '').replace('Km', '') # 주행거리
    displacement = data[4]
    
    caryear = data[1].split()[0] + ' ' + data[1].split()[1] # 연식
    carcolor = data[6]
    carfuel = data[2] # 연료
    
    # 사진 가져오기
    filename = carnumber

    picturexpath = '//*[@id="carPic"]/span/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')
    imglink = "carimg/encar/" + filename + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    #url 모바일로 변경
    mobile_url = 'https://fem.encar.com/cars/detail/CARID?listAdvType=share&adnm=mo_detail_url'
    id_start = url.find('carid') + 6
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



    
