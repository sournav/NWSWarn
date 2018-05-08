from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from warn_wrap import warn_wrap as ww
class currwarn(ww):
    def __init__(self):
        self.url='https://alerts.weather.gov/cap/us.php?x=1?map=on'
        self.page=urlopen(self.url)
        self.soup = bs(self.page,'xml')
        self.tags = ['event',
                         'effective',
                         'expires',
                         'status',
                         'msgType',
                         'category',
                         'urgency',
                         'severity',
                         'certainty',
                         'areadesc',
                         'polygon',
                         'summary']
    def xml2str_small(self,string,tagsize):
        return str(string)[tagsize:][:(-1*tagsize-1)]
    def xml2str(self,arr,tagsize):
        arr_str=[]
        for i in arr:
            arr_str.append(str(i)[tagsize:][:(-1*tagsize-1)])
            #print(i)
        return arr_str
    def getCurrWarn(self,strdat='',strfilt='',condition=''):
        if strdat=='':
            ret=[]
            entries=self.soup.find_all('entry')
            for i in entries:
                #print(str(i))
                temp_soup=bs(str(i),'lxml')
                temp=[]
                for j in self.tags:
                    events_xml=temp_soup.find('cap:'+j)
                    taglength = len(j)
                    events_str=self.xml2str_small(events_xml,taglength+6)
                    temp.append(events_str)
                ret.append(temp)
            
            #events_str=self.xml2str(events_xml,taglength+6)
            #self.cap_dict[strdat]=events_str
            return ret
        elif strfilt=='' and condition=='':
            events_xml=self.soup.find_all('cap:'+strdat)
            taglength = len(strdat)
            events_str=self.xml2str(events_xml,taglength+6)
            #self.cap_dict[strdat]=events_str
            return events_str
        else:
            events_xml=self.soup.find_all('cap:'+strdat)
            events_xml2=self.soup.find_all('cap:'+strfilt)
            taglength = len(strdat)
            taglength2 = len(strfilt)
            events_str=self.xml2str(events_xml,taglength+6)
            events_str2=self.xml2str(events_xml2,taglength2+6)
            #self.cap_dict[strdat]=events_str
            lent=len(events_str)
            ret_arr=[]
            for i in range(lent):
                #print(events_str2[i],condition)
                if events_str2[i]==condition:
                    ret_arr.append(events_str[i])
            return ret_arr
    #def getCurrWarn(self,strdat):
        
    
    #def getCurrWarn(self,strdat,strfilt,condition):
        
    
    def availabletags(self):
        return self.cap_tags
    def findwarn(x):
        page = urlopen('https://alerts.weather.gov/cap/wwaatmget.php?x='+x+'&amp')
        soup = bs(page,'lxml')
        alert = soup.find_all('title')
        warning = str(alert[1])[7:][:-8]
        return warning
    

##x = currwarn()
##cap=x.getCurrWarn('event','urgency','Expected')
##
###cap = soup.find_all('cap:polygon')
##print(x.getCurrWarn())
