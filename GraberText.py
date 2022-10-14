import lxml.html
import requests
import UArand
import time
import textproxyconf
import logging
log = logging.getLogger('Proxy_Graber')

urllist=textproxyconf.proxysitelist


def getlist(url):
    error=0
    proxy=[]
    try:
        page = requests.get(url, headers = UArand.randomua())
        tree = lxml.html.fromstring(page.text)
    except:
        error=1
        return error, proxy
    collist = tree.xpath('//*/text()')
    lproxy=collist[0].split('\r\n')
    colp=len(lproxy)-1
    del lproxy[colp]
    for i in range(len(lproxy)):
        proxyr={}
        temp=lproxy[i]
        proxyr['ip']=temp.split(':')[0]
        proxyr['port']=temp.split(':')[1]
        proxy.append(proxyr)
    return error, proxy


def main():
    tempt=time.time()
    proxy=[]
    for i in range(len(urllist)-1):
        error, templ=getlist(urllist[i])
        if error==0:
            for n in range(len(templ)-1):
                tempp=templ[n]
                proxy.append(tempp)
    log.info('Прокси украдены за: %sс. %sшт.'%(time.time()-tempt,len(proxy)))
    return proxy

