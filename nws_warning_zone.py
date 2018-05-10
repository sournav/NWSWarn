"""
MADE BY SOURNAV SEKHAR BHATTACHARYA
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from warn_wrap import warn_wrap as ww

"""
This class represents current warnings.
You can instantiate it and use member functions to get
current warnings, and more.
Extends the warn_wrap abstract class
"""
class currwarn(ww):
    """
    Constructor for the currwarn class, opens NWS warning page,
    and initializes all possible tags for the given weather warning site
    """
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
                         'areaDesc',
                         'polygon',
                         'summary',
                         'state',
                         'fips']
    """
    xml2str_small used to convert a given xml line (including the tag itself) to string
    """
    def xml2str_small(self,string,tagsize):
        return str(string)[tagsize:][:(-1*tagsize-1)]
    """
    Does the same thing as xml2str_small but over multiple entries in an array of
    items with the same tag
    """
    def xml2str(self,arr,tagsize):
        arr_str=[]
        for i in arr:
            arr_str.append(str(i)[tagsize:][:(-1*tagsize-1)])
            #print(i)
        return arr_str
    """
    Gets a 2 digit state postal code depending
    on geocode provided in cap feed
    """
    def geo2state(self,xml_inp):
        soup=bs(str(xml_inp),'lxml')
        value=soup.find_all('value')[1]
        value_str=self.xml2str_small(value,7)
        return value_str[0:2]
    """
    Gets a 2 digit state postal code depending
    on geocode provided in cap feed
    """
    def geo2fips(self,xml_inp):
        soup=bs(str(xml_inp),'lxml')
        value=soup.find_all('value')[0]
        value_str=self.xml2str_small(value,7)
        return value_str[1:6]
    """
    Gets current warnings. Impliments function overloading.
    If no fields are specified then it gets an array of all
    possible tags.
    If strfilt and strfilt are left empty then it returns all values
    of a certain type of cap value
    If strfilt, and condition are filled then an array of cap data filtered by
    the given condition
    """
    def getCurrWarn(self,strdat='',strfilt='',condition=''):
        if strdat=='' and strfilt=='' and condition=='':
            ret=[]
            
            entries=self.soup.find_all('entry')
            #FOR TESTING PURPOSES
            ##print(entries)
            #END TESTING
            for i in entries:
                
                temp_soup=bs(str(i),'lxml')
                temp=[]
                for j in self.tags:
                    if j not in ['state','fips']:
                        #seperate cap values in an entry
                        events_xml=temp_soup.find('cap:'+j.lower())
                        taglength = len(j)
                        events_str=self.xml2str_small(events_xml,taglength+6)
                        temp.append(events_str)
                    else:
                        if j=='state':
                            events_xml=temp_soup.find('cap:geocode')
                            temp.append(self.geo2state(events_xml))
                            continue
                        if j=='fips':
                            events_xml=temp_soup.find('cap:geocode')
                            temp.append(self.geo2fips(events_xml))
                            break
                ret.append(temp)
                
            
            
            return ret
        elif strfilt=='' and condition=='':
            if j not in ['state','fips']:
                events_xml=self.soup.find_all('cap:'+strdat)
                taglength = len(strdat)
                events_str=self.xml2str(events_xml,taglength+6)
                
                return events_str
        else:
            ret=[]
            entries=self.soup.find_all('entry')
            for i in entries:
                
                temp_soup=bs(str(i),'lxml')
                temp=[]
                for j in self.tags:
                    if j not in ['state','fips']:
                        events_xml=temp_soup.find('cap:'+j.lower())
                        taglength = len(j)
                        events_str=self.xml2str_small(events_xml,taglength+6)
                        temp.append(events_str)
                    else:
                        if j=='state':
                            events_xml=temp_soup.find('cap:geocode')
                            temp.append(self.geo2state(events_xml))
                            continue
                        if j=='fips':
                            events_xml=temp_soup.find('cap:geocode')
                            temp.append(self.geo2fips(events_xml))
                            break
                    
                if condition in temp:
                        ret.append(temp)
            return ret
            
        
    """
    Returns all available tags
    """
    def availabletags(self):
        return self.tags
    """
    Use this to find current warning state given a specific area code
    """
    def findwarn(x):
        page = urlopen('https://alerts.weather.gov/cap/wwaatmget.php?x='+x+'&amp')
        soup = bs(page,'lxml')
        alert = soup.find_all('title')
        warning = str(alert[1])[7:][:-8]
        return warning
    
#TEST CODE
x = currwarn()
##cap=x.getCurrWarn('event','urgency','Expected')
##
###cap = soup.find_all('cap:polygon')
#x.getCurrWarn()
#print(x.getCurrWarn())
#import time
#start=time.time()
#y=x.getCurrWarn()
#end=time.time()
#print(str(end-start))
