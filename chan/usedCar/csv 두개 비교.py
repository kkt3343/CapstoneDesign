import csv
from edit_distance import edit_distance

f1 = open('엔카모델명.csv', 'r')
reader1 = csv.reader(f1)
f2 = open('모델명 통합 정리4.csv', 'r')
reader2 = csv.reader(f2)
f2rows = list(reader2)

data = []
for f1row in reader1:
    m = 1000
    m_row = []
    for f2row in f2rows:
        d = edit_distance(f1row[2], f2row[2])
        if d < m:
            m = d
            m_row = f2row

    if m <= 3:
        model = m_row[1]
        model_detail = m_row[2]

    data.append([f1row[0], f1row[1], f1row[2], m_row[0], m_row[1], m_row[2]])


f3 = open('엔카 통합 모델명 비교.csv', 'w')
writer = csv.writer(f3)

writer.writerows(data)
f1.close()
f2.close()
f3.close()
