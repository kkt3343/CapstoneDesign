import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
from edit_distance import edit_distance

def diagnosed_item(url, conn, cur, driver): #진단 매물
    time.sleep(2)

    # 타이틀 가져오기
    text = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/strong').text

    # 차번호
    carnumber = text[1:text.find(')')]

    text = text[text.find(')') + 1:]
    title = text.replace('\n', ' ')

    # 사이트 분류
    site = 'KB'

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        print('중복 매물입니다.')
        return

    # 차종
    cartype = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[4]/td[1]').text


    # 제조사
    titleList = title.split()
    searchWord = ''
    manufacturer = ''

    for i in range(len(titleList)):
        searchWord += titleList[i]
        if searchWord == '한국GM':
            manufacturer = '쉐보레(GM대우)'
            break
        sql = 'SELECT DISTINCT manufacturer FROM carModel WHERE manufacturer = "{0}"'
        sql = sql.format(searchWord)
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) == 1:
            manufacturer = rows[0][0]
            break
        searchWord += ' '

    if manufacturer == '':
        print('제조사 구분 중 오류 발생')
        print(title)
        return

    # 모델명 확인
    head_title = driver.find_element_by_xpath('/html/head/title').get_attribute('innerText')
    head_title = head_title[:head_title.find('가격')]
    head_title = head_title.replace('한국GM', '')
    searchWord = head_title.replace(manufacturer, '').strip()
    model_detail = ''

    sql = 'SELECT * FROM carModel WHERE manufacturer = "{0}" and model_detail = "{1}"'
    sql = sql.format(manufacturer, searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        model = rows[0][1]
        model_detail = rows[0][2]

    if model_detail == '':
        sql = 'SELECT * FROM carModel WHERE manufacturer = "{0}"'
        sql = sql.format(manufacturer)
        cur.execute(sql)
        rows = cur.fetchall()
        m = 1000
        for row in rows:
            d = edit_distance(searchWord, row[2])
            if d < m:
                m = d
                m_row = row

        if m < 4:
            print('편집 거리 사용')
            model = m_row[1]
            model_detail = m_row[2]
            
        if model_detail == '':
            print('모델 구분 중 오류 발생!')
            print(title)
            return

    # 가격
    temp = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/dl/dd/strong').text

    temp = temp.replace(",", "")
    temp = temp.replace("만원", "0000")
    price = int(temp)

    # 거리
    distance = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[2]/td[1]').text
    distance = distance.replace(",", "")
    distance = distance.replace('km', "")

    # 배기량
    displacement = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[4]/td[2]').text

    # 연식
    caryear = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[1]/td[2]').text
    caryear = caryear.split('(')[0]
    caryear = caryear.replace('년', '년 ') + '식'

    # 색
    carcolor = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[5]/td[1]').text

    # 연료
    carfuel = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[8]/div/div[1]/table/tbody/tr[2]/td[2]').text

    # 사진 가져오기
    filename = carnumber

    picturexpath = '//*[@id="btnCarPhotoView"]/li[2]/div[1]/a/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')
    imglink = "carimg/KB/" + filename + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    # url 모바일로 변경
    mobile_url = 'https://m.kbchachacha.com/public/web/car/detail.kbc?carSeq=CARID'
    id_start = url.find('carSeq') + 7

    carid = url[id_start:]
    mobile_url = mobile_url.replace('CARID', carid)

    # DB에 저장
    sql = 'insert into usedCar values(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", {8}, {9}, "{10}", "{11}", "{12}", "{13}", "{14}")'
    sql = sql.format(mobile_url, site, title, carnumber, cartype, manufacturer, model, model_detail, price, distance,
                     displacement, caryear, carcolor, carfuel, imglink)
    cur.execute(sql)
    conn.commit()


def normal_item(url, conn, cur, driver):  # 일반등록 매물
    time.sleep(2)

    # 타이틀 가져오기
    text = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/strong').text

    # 차번호
    carnumber = text[1:text.find(')')]

    text = text[text.find(')') + 1:]
    title = text.replace('\n', ' ')

    # 사이트 분류
    site = 'KB'

    # 차번호로 중복체크
    sql = 'SELECT * FROM usedCar WHERE carnumber = "{0}"'.format(carnumber)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        print('중복 매물입니다.')
        return

    # 차종
    cartype = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[4]/td[1]').text

    # 제조사
    titleList = title.split()
    searchWord = ''
    manufacturer = ''

    for i in range(len(titleList)):
        searchWord += titleList[i]
        if searchWord == '한국GM':
            manufacturer = '쉐보레(GM대우)'
            break
        sql = 'SELECT DISTINCT manufacturer FROM carModel WHERE manufacturer = "{0}"'
        sql = sql.format(searchWord)
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) == 1:
            manufacturer = rows[0][0]
            break
        searchWord += ' '

    if manufacturer == '':
        print('제조사 구분 중 오류 발생')
        print(title)
        return

    # 모델명 확인
    head_title = driver.find_element_by_xpath('/html/head/title').get_attribute('innerText')
    head_title = head_title[:head_title.find('가격')]
    head_title = head_title.replace('한국GM', '')
    searchWord = head_title.replace(manufacturer, '').strip()
    model_detail = ''

    sql = 'SELECT * FROM carModel WHERE manufacturer = "{0}" and model_detail = "{1}"'
    sql = sql.format(manufacturer, searchWord)
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 1:
        model = rows[0][1]
        model_detail = rows[0][2]

    if model_detail == '':
        sql = 'SELECT * FROM carModel WHERE manufacturer = "{0}"'
        sql = sql.format(manufacturer)
        cur.execute(sql)
        rows = cur.fetchall()
        m = 1000
        for row in rows:
            d = edit_distance(searchWord, row[2])
            if d < m:
                m = d
                m_row = row

        if m < 4:
            print('편집 거리 사용')
            model = m_row[1]
            model_detail = m_row[2]
            
        if model_detail == '':
            print('모델 구분 중 오류 발생!')
            print(title)
            return

    # 가격
    temp = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/dl/dd/strong').text
    temp = temp.replace(",", "")
    temp = temp.replace("만원", "0000")
    price = int(temp)

    # 거리
    distance = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[2]/td[1]').text
    distance = distance.replace(",", "")
    distance = distance.replace('km', "")

    # 배기량
    displacement = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[4]/td[2]').text

    # 연식
    caryear = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[1]/td[2]').text
    caryear = caryear.split('(')[0]
    caryear = caryear.replace('년', '년 ') + '식'

    # 색
    carcolor = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[5]/td[1]').text

    # 연료
    carfuel = driver.find_element_by_xpath(
        '//*[@id="content"]/div[1]/div[2]/div[2]/div[5]/div/div[1]/table/tbody/tr[2]/td[2]').text

    # 사진 가져오기
    filename = carnumber

    picturexpath = '//*[@id="btnCarPhotoView"]/li[2]/div[1]/a/img'
    img = driver.find_element_by_xpath(picturexpath).get_attribute('src')
    imglink = "carimg/KB/" + filename + ".jpg"
    urllib.request.urlretrieve(img, "C:/xampp/htdocs/" + imglink)

    # url 모바일로 변경
    mobile_url = 'https://m.kbchachacha.com/public/web/car/detail.kbc?carSeq=CARID'
    id_start = url.find('carSeq') + 7

    carid = url[id_start:]
    mobile_url = mobile_url.replace('CARID', carid)

    # DB에 저장
    sql = 'insert into usedCar values(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", {8}, {9}, "{10}", "{11}", "{12}", "{13}", "{14}")'
    sql = sql.format(mobile_url, site, title, carnumber, cartype, manufacturer, model, model_detail, price, distance,
                     displacement, caryear, carcolor, carfuel, imglink)
    cur.execute(sql)
    conn.commit()
