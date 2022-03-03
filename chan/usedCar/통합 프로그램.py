import threading
import KB_crawler
import encar_crawler
import kcar_crawler
import bobae_crawler
import time

hostip = '10.91.40.85'

# i 값에 따라
i = 1

# 0 : 엔카
encar_start_page = 1
encar_end_page = 15

# 1 : KB_차차차
kb_start_page = 1
kb_end_page = 20

# 2 : 케이카
kcar_start_page = 1
kcar_end_page = 15

# 3 : 보배드림
bobae_start_page = 1
bobae_end_page = 15


while True:
    if i == 0:
        t = threading.Thread(target=encar_crawler.start_crawling, args=(hostip, 300, encar_start_page, encar_end_page))
        t.start()
        t.join()
    elif i == 1:
        t = threading.Thread(target=KB_crawler.start_crawling, args=(hostip, 300, kb_start_page, kb_end_page))
        t.start()
        t.join()
    elif i == 2:
        t = threading.Thread(target=kcar_crawler.start_crawling, args=(hostip, 300, kcar_start_page, kcar_end_page))
        t.start()
        t.join()
    elif i == 3:
        t = threading.Thread(target=bobae_crawler.start_crawling, args=(hostip, 300, bobae_start_page, bobae_end_page))
        t.start()
        t.join()

    time.sleep(90)
    i = (i + 1) % 4
