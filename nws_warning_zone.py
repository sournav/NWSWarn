from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
search_page = 'https://alerts.weather.gov/cap/wwaatmget.php?x=AKZ181&amp'
def findwarn(x):
    page = urlopen(x)
    soup = bs(page,'lxml')
    alert = soup.find_all('title')
    warning = str(alert[1])[7:][:-8]
    return warning
print(findwarn(search_page))
