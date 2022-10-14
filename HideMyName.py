import lxml.html
import requests
import UArand
import time
import logging
log = logging.getLogger('Proxy_Graber')

def getcollist(list=None):
    if 0!=list!=None:
        pcoll=list*2-64
        page = requests.get(f'https://hidemy.name/ru/proxy-list/?start={pcoll}#list', headers = UArand.randomua())
    else:
        page = requests.get('https://hidemy.name/ru/proxy-list/?start=0#list', headers = UArand.randomua())
    tree = lxml.html.document_fromstring(page.text)
    collist = tree.xpath('//*[@class="pagination"]/ul/li[9]/a/text()')
    ip = tree.xpath('//*[@class="table_block"]/table/tbody/tr/td[1]/text()')
    port= tree.xpath('//*[@class="table_block"]/table/tbody/tr/td[2]/text()')
    proxy=[]
    for i in range(len(ip)):
        proxyr={}
        proxyr['ip']=ip[i]
        proxyr['port']=port[i]
        proxy.append(proxyr)

    if 0!=list!=None: return proxy
    else: return collist[0],proxy


def main():
    stime=time.time()
    lists, proxy=getcollist()
    i=2
    while i<=int(lists):
        tproxy=getcollist(i)
        for n in range(len(tproxy)):
            proxy.append(tproxy[n])
        i+=1
    log.info('Прокси украдены с HideMy.name за: %sс. %sшт.'%(time.time()-stime,len(proxy)))
    return proxy