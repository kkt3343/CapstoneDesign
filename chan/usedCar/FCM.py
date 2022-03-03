from pyfcm import FCMNotification
 
APIKEY = "AAAAZrIxOQ0:APA91bHZeXbrwNbymAzL3rSkMzUxqtpoNtBFe5uc5zMX2oLbCrhTn0aUUYTzmfmjEhI_snUnWnL8e-IKXeXTcKVGVFv7bvfm8ErDbh42cyl8HHHvk-il0jaiJlpt1vGeOglvJjP7WgVU"
TOKEN = "dNPXbXFeSwelqItxFsl4N3:APA91bECTzwLUtuQcL2Xp5A87dIKjtUKsnYSZj_E1yaEohSyDaypO0rDxPGF0EOdQDBI7pD4IZOfLI_3_ewxdNFMzAxOQEdtTTEuZINgx-4R4Zh-s4T9bSE6926z8i9WxlqfmdTXZ1Zh"
 
# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)
 
def sendMessage(body, title):
    # 메시지 (data 타입)
    data_message = {
        "body": body,
        "title": title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    result = push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)
 
    # 전송 결과 출력
    print(result)
 
sendMessage("배달의 민족", "치킨 8000원 쿠폰 도착!")
