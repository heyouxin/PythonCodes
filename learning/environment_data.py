from bs4 import BeautifulSoup
import requests
'''
from bs4 import BeautifulSoup
fileName = 'C:/Users/heyouxin/Desktop/examples.csv'
for page in range(0,100):
    url_1 = 'http://esf.xm.fang.com/house/i3'
    url_2 = str(page)
    url_3 = '/'
    url = ''.join([url_1,url_2,url_3])
    html = requests.get(url).content

    soup = BeautifulSoup(html,'lxml')
    container = soup.find('div', attrs={'class': 'houseList'}).find_all('dl')
    for each in container:
        href = 'http://esf.xm.fang.com' + each.find('dt').find('a')['href']

        h = requests.get(href).content
        soup = BeautifulSoup(h)
        info2 = soup.find('div', attrs={'class': 'inforTxt'}).find_all('dl')[0].getText().encode('GB18030')
        print(info2)
        info3 = soup.find('div', attrs={'class': 'inforTxt'}).find_all('dl')[1].getText().encode('GB18030')
        print(info3)
        with codecs.open(fileName, 'ab') as f:
            writer = csv.writer(f)
            writer.writerow((info2, info3))


'''
url='http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city=&startdate=2014-01-01&enddate=2017-02-06&page=2'
html = requests.get(url).content
soup = BeautifulSoup(html,'html.parser')
table_data=soup.select("#report1")
print(table_data)


