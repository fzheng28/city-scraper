from string import ascii_lowercase
from collections import namedtuple
from time import sleep
import string
import re
from itertools import permutations
import random import randint 
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://www.wdfi.org/apps/CorpSearch/Results.aspx?type=Advanced&nameSet=Entities&q={}&textSearchType=StartsWith&incDateStart={}&includeActiveOrgs=Include&includeOldNames=Exclude&orgTypes='
MIN_WAIT = 60
MAX_WAIT = 90
Corporation = namedtuple('Corporation', ['id', 'effective_date', 'status', 'status_date', 'type', 'agent_in_madison', 'office_in_madison','agent_zip','office_zip'])



def get_batch(letter_combo, start_date):
    # it is fine to not translate the formate of the date 
    # as the website link will read it into month%2fday%2fyear automaticly
    url = BASE_URL.format(letter_combo, start_date)
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text,'html.parser')
    # a list of detail link
    detail_urls =[]
    for a in soup.find_all('a', href=True):
        # there could be mutiple links 
        # so only keep the ones that begins with Details.aspx?entityID=
        # append those into a list 
        if a['href'].startswith( 'Details.aspx?entityID=' ):
            detail_urls.append(a['href'])
    return detail_urls # a list of detail_urls


# data cleaning and zip code finder
def data_clean(string):
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = string.replace('\t','')
    string = string.replace('   ','')
    string = string.replace('  Request a Certificate of Status','')
    return string

def data_clean_loc(string):
    string = string.lower()
    match =r'\r\n  *madison\r\n  *,\r\n  *wi\r\n  *[0-9]{5}\r\n'
    if re.search(match, string):
        return 'Yes'
    else:
        return 'No'
    
def zip_code(string):
    match =r'  *5[0-9]{4}'
    if len(re.findall(gmail_re, text)) == 0:
        return "None"
    else:
        return re.findall(gmail_re, text)[0]
    

# create Corporation object for each company; need to check zip 
def get_detail(detail_url):

    url = 'https://www.wdfi.org/apps/CorpSearch/'+detail_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    a=soup.find_all('table', class_='stats')
    li={}
    for table in a:
        rows=table.findAll('tr')
      
        corporation= Corporation
         
        for row in rows:
            try:
                label = row.findAll('td', class_= 'label')[0].getText()
                data = row.findAll('td', class_= 'data')[0].getText()
            except IndexError:    
                continue
           
            label = label.replace('\r','')
            label = label.replace('\n','')
            label = label.replace('\t','')
            label = label.replace(' ','')
            if label =='EntityID':
                corporation.id = data_clean(data)
            elif label == 'RegisteredEffectiveDate':
                corporation.effective_date=data_clean(data)
            elif label =='Status':
                corporation.status=data_clean(data)
            elif label == 'StatusDate':
                corporation.status_date=data_clean(data)
            elif label == 'EntityType':
                corporation.type = data_clean(data)
            elif label == 'RegisteredAgentOffice':
                corporation.agent_in_madison = data_clean_loc(data)
            elif label == 'PrincipalOffice':
                corporation.office_in_madison = data_clean_loc(data)
            elif label == 'RegisteredAgentOffice':
                corporation.agent_zip = zip_code(data)
            elif label == 'PrincipalOffice':
                corporation.office_zip = zip_code(data)
    return corporation

# convert tuple to string
def convertTuple(tup): 
    string =  ''.join(tup) 
    return string

# test for now as 26 letters generate too many combinations  
# perm = permutations[list(string.ascii_lowercase), 3]

# tie everything together 
def main(start_date): # start_date need to be in string month/day/year format
    corporations = []
    perm = permutations(ascii_lowercase,3)
    for i in list(perm): 
        batch = get_batch(convertTuple(i),start_date)
        sleep(randint(MIN_WAIT,MAX_WAIT))
        for links in batch:
            for link in links:
                detail = get_detail(link)
                sleep(randint(MIN_WAIT,MAX_WAIT))
                corporations.append(detail)
    return(corporations) 



