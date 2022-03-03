import pymysql
import csv

conn = pymysql.connect(host='localhost', user='root', password='xoduqrb', db='usedcardb', charset='utf8')
cur = conn.cursor()

f = open('엔카 정리_ver_20220129.csv', 'r', encoding='utf-8-sig')
reader = csv.reader(f)
rows = list(reader)

count = 0
for row in rows:
    count += 1
    if count >= 3 and row[0] != '':
        manufacturer1 = row[0]
        model1 = row[1]
        model_detail1 = row[2]
        
        manufacturer2 = row[3]
        model2 = row[4]
        model_detail2 = row[5]
        
        sql = 'insert into EncarModel values("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'
        sql = sql.format(manufacturer1, model1, model_detail1, manufacturer2, model2, model_detail2)
        cur.execute(sql)
        conn.commit()

f.close()
conn.close()
