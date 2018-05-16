from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from warn_wrap import warn_wrap as ww
class currwarn(ww):

    def __init__(self):
        self.warning=[]
        page = urlopen('https://weather.gc.ca/warnings/')
        soup = bs(page,'lxml')
        table = soup.table
        table_rows = table.find_all('tr')
        self.tags =     ['event',
                         'effective',
                         'expires',
                         'status',
                         'msgType',
                         'category',
                         'urgency',
                         'severity',
                         'certainty',
                         'areaDesc',
                         'polygon',
                         'geocode',
                         'parameter',
                         'summary',
                         'brief']
        for tr in table_rows:
            td=tr.find_all('td')
            self.warning.append([str(i.text).replace('\n','').replace('\xa0','N/A')
                                 for i in td])

    def getCurrWarn(self,filt=''):
        ret=[]
        if filt=='':
            return self.warning
        for i in self.warning:
            temp=0
            for j in i:
                if j==filt:
                    temp=1
                    break
            if temp==1:
                ret.append(i)
        return ret

    def findwarn(x):
        warning=[]
        page = urlopen('https://weather.gc.ca/rss/battleboard/'+x+'_e.xml')
        soup = bs(page,'lxml')
        alert = soup.find_all('title')
        for i in alert:
            warning.append(str(i)[7:][:-8])
        return warning[1:]
            
x=currwarn()
print(x.getCurrWarn())
