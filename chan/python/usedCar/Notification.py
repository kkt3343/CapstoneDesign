import pymysql
from pyfcm import FCMNotification

def notify(conn, cur, title, model, caryear, distance, price):
    APIKEY = "AAAAZrIxOQ0:APA91bHZeXbrwNbymAzL3rSkMzUxqtpoNtBFe5uc5zMX2oLbCrhTn0aUUYTzmfmjEhI_snUnWnL8e-IKXeXTcKVGVFv7bvfm8ErDbh42cyl8HHHvk-il0jaiJlpt1vGeOglvJjP7WgVU"
    caryear = caryear[:2]
    if int(caryear) > 22:
        caryear = "19" + caryear
    else:
        caryear = "20" + caryear
        
    sql = 'SELECT DISTINCT userid FROM Notification WHERE model = "{0}" '
    sql = sql + 'and (caryear_from is NULL or caryear_from <= {1}) and (caryear_to is NULL or {1} <= caryear_to) '
    sql = sql + 'and (distance_from is NULL or distance_from <= {2}) and (distance_to is NULL or {2} <= distance_to) '
    sql = sql + 'and (price_from is NULL or price_from <= {3}) and (price_to is NULL or {3} <= price_to)'
    sql = sql.format(model, caryear, distance, price)
    #print("sql :", sql)
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        userid = row[0]
        sql2 = 'SELECT token FROM userTable WHERE userid = "{0}"'.format(userid)
        #print("sql2 :", sql2)
        if cur.execute(sql2) > 0:
            row2 = cur.fetchall()[0]
            if row2[0] is not None:
                TOKEN = row2[0]
                push_service = FCMNotification(APIKEY)
                data_message = {
                    "body": "자동차 가격 비교",
                    "title": title
                }
                result = push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)
                print(result)


        
