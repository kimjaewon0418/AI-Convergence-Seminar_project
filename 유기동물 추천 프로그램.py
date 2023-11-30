import csv
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote

tags = ['age', 'careAddr', 'careNm', 'careTel', 'chargeNm', 'colorCd',
        'desertionNo', 'filename', 'happenDt', 'happenPlace', 'kindCd',
        'neuterYn', 'noticeEdt', 'noticeNo', 'noticeSdt', 'officetel',
        'orgNm', 'popfile', 'processState', 'sexCd', 'specialMark', 'weight']
animals = []
count = 0

def find_tag(element):
    global count
    global tags
    animal = {}
    
    for tag in tags:
        try:
            tmp = element.find(tag)
            animal[tag] = tmp.text
        except AttributeError as e:
            animal[tag] = 'not info'
            count+=1
    return animal


for i in range(1, 5+1): #1~20
    url = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic'
    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey') : '89tnGVYuR/qYSc64GB220TOHrrltq/aMJ8SBksKW60ag5yj51XjWcmdS4b0eRDJPguo9n0EeJ8ClPL6vWOPzNA==',
            quote_plus('bgnde') : '20140601', #발견날짜
            quote_plus('kind') : '000114',     #품종
            quote_plus('upr_cd') : '6420000',   #지역
            quote_plus('pageNo') : '%d'%i,
            quote_plus('numOfRows') : '20'
        }
    )

    request = Request(url + queryParams)
    response = urlopen(request)
    rescode = response.getcode()

    if(rescode == 200):
        res = response.read()
        xml = res.decode('utf-8')

    root = ET.fromstring(xml)
    item = root.iter(tag="item")
    
    for element in item:
        animal = find_tag(element)
        animals.append(animal)
            
    print('Collect info %d page'%i)

print('Create 강원도+믹스견.csv file..')
tag = ['careAddr', 'kindCd', 'happenDt', 'neuterYn']
f = open('강원도+믹스견.csv', 'w', newline='')
w = csv.writer(f)
w.writerow(['num'] + tag)
for i in range(400):
    arr = ['%d'%i]
    for j in tag:
        arr.append(animals[i][j])
    w.writerow(arr)
f.close()
print('**** Success Collect 400 Aniamls Info! ****')
