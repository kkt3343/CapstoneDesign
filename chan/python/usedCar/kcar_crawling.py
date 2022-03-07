import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from edit_distance import edit_distance
from Notification import notify

def direct_sales(url, conn, cur, driver): #직영 매물
    time.sleep(2)

    site = '케이카'
    title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/h2').text
    carnumber = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[1]/strong').text

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        print('중복 매물입니다.')
        return
    
    cartype = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[8]/strong').text

    #모델명 확인
    searchWord = driver.find_element_by_xpath('//*[@id="container"]/form[6]/input[12]').get_attribute('value')
    model_detail = ''

    sql = 'SELECT * FROM KCarModel WHERE model_detail1 = "{0}"'
    sql = sql.format(searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        manufacturer = rows[0][3]
        model = rows[0][4]
        model_detail = rows[0][5]

    else:
        print('모델명 구분 실패!')
        return
    
    #가격 저장
    temp = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[3]/div[1]/span').text
    price = temp.split()[-1]
    price = price.replace(',', '').replace('만원', '0000')

    distance = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[5]/strong').text
    distance = distance.replace('Km', '').split(',')
    if len(distance) == 1:
        distance = distance[0]
    else:
        distance = distance[0] + distance[1]

    displacement = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[2]/strong').text
    carcolor = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[4]/strong').text
    caryear = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/span[2]').text
    carfuel = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[7]/strong').text

    # 사진 가져오기
    picturexpath = '//*[@id="carImgSlider"]/li[1]/a/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')
    imglink = "carimg/kcar/" + carnumber + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    #url 모바일로 변경
    mobile_url = 'https://m.kcar.com/mobile/carinfo/car_detail.do?i_sCarCd=CARID'
    carid = driver.find_element_by_xpath('//*[@id="i_sCarCd"]').get_attribute('value')
    mobile_url = mobile_url.replace('CARID', carid)
    
    # DB에 저장
    sql = 'insert into usedCar values(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", {8}, {9}, "{10}", "{11}", "{12}", "{13}", "{14}")'
    sql = sql.format(mobile_url, site, title, carnumber, cartype, manufacturer, model, model_detail, price, distance, displacement, caryear, carcolor, carfuel, imglink)
    cur.execute(sql)
    conn.commit()
    notify(conn, cur, title, model, caryear, distance, price)

def _3d_sales(url, conn, cur, driver): # 3d 뷰 제공 매물
    time.sleep(2)

    site = '케이카'
    title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/h2').text
    carnumber = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[1]/strong').text

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        print('중복 매물입니다.')
        return
    
    cartype = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[8]/strong').text

    #모델명 확인
    searchWord = driver.find_element_by_xpath('//*[@id="container"]/form[6]/input[12]').get_attribute('value')
    model_detail = ''

    sql = 'SELECT * FROM KCarModel WHERE model_detail1 = "{0}"'
    sql = sql.format(searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        manufacturer = rows[0][3]
        model = rows[0][4]
        model_detail = rows[0][5]

    else:
        print('모델명 구분 실패!')
        return
    
    #가격 저장
    temp = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[3]/div[1]/span').text
    price = temp.split()[-1]
    price = price.replace(',', '').replace('만원', '0000')

    distance = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[5]/strong').text
    distance = distance.replace('Km', '').split(',')
    if len(distance) == 1:
        distance = distance[0]
    else:
        distance = distance[0] + distance[1]

    displacement = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[2]/strong').text
    carcolor = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[4]/strong').text
    caryear = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/span[2]').text
    carfuel = driver.find_element_by_xpath('//*[@id="content"]/div[3]/section[3]/div[2]/ul/li[7]/strong').text

    # 사진 가져오기
    text = ''
    container = driver.find_element_by_xpath('//*[@id="container"]')
    scripts = container.find_elements_by_tag_name('script')
    for script in scripts:
        if script.get_attribute('innerText').find('carPic = "') != -1:
            text = script.get_attribute('innerText')
    if text != '':
        img = text.split('carPic = "')[1].split('";')[0]
    picturexpath = '//*[@id="carImgSlider"]/li[1]/a/img'
    imglink = "carimg/kcar/" + carnumber + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    #url 모바일로 변경
    mobile_url = 'https://m.kcar.com/mobile/carinfo/car_detail.do?i_sCarCd=CARID'
    carid = driver.find_element_by_xpath('//*[@id="i_sCarCd"]').get_attribute('value')
    mobile_url = mobile_url.replace('CARID', carid)
    
    # DB에 저장
    sql = 'insert into usedCar values(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", {8}, {9}, "{10}", "{11}", "{12}", "{13}", "{14}")'
    sql = sql.format(mobile_url, site, title, carnumber, cartype, manufacturer, model, model_detail, price, distance, displacement, caryear, carcolor, carfuel, imglink)
    cur.execute(sql)
    conn.commit()
    notify(conn, cur, title, model, caryear, distance, price)
