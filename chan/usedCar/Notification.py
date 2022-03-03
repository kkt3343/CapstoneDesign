import pymysql
from pyfcm import FCMNotification

def notify(conn, cur, title, model, caryear, distance, price):
    APIKEY = "AAAAZrIxOQ0:APA91bHZeXbrwNbymAzL3rSkMzUxqtpoNtBFe5uc5zMX2oLbCrhTn0aUUYTzmfmjEhI_snUnWnL8e-IKXeXTcKVGVFv7bvfm8ErDbh42cyl8HHHvk-il0jaiJlpt1vGeOglvJjP7WgVU"

    sql = 'SELECT * FROM Notification WHERE model = "{0}"'.format(model)
    print("sql :", sql)
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        userid = row[1]
        sql2 = 'SELECT token FROM userTable WHERE userid = "{0}"'.format(userid)
        print("sql2 :", sql2)
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


        
