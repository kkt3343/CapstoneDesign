import pymysql
import csv

conn = pymysql.connect(host='localhost', user='root', password='xoduqrb', db='usedcardb', charset='utf8')
cur = conn.cursor()

f = open('모델명 통합 정리_ver_20220129.csv', 'r')
reader = csv.reader(f)
rows = list(reader)
for row in rows:
    manufacturer = row[0]
    model = row[1]
    model_detail = row[2]
    sql = 'insert into carModel values("{0}", "{1}", "{2}")'
    sql = sql.format(manufacturer, model, model_detail)
    cur.execute(sql)
    conn.commit()

f.close()
conn.close()
