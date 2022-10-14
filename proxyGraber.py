import requests
from bs4 import BeautifulSoup
import UArand
import time
import logging
log = logging.getLogger('Proxy_Graber')

def main(url):
  stime=time.time()
  proxies_req = requests.get(url, headers = UArand.randomua())
  soup = BeautifulSoup(proxies_req.text, 'html.parser')

  proxies_table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
  prod = proxies_table.find("tbody")
 
  proxy=[]
  for row in prod.find_all('tr'):
    proxyr={}
    proxyr['ip']=row.find_all('td')[0].string
    proxyr['port']=row.find_all('td')[1].string
    proxy.append(proxyr)

  log.info('Прокси украдены с %s за: %sс. %sшт.'%(url,time.time()-stime,len(proxy)))
  return proxy