import time
import requests
import proxyGraber
import HideMyName
import GraberText
import logging
import os

log = logging.getLogger('Proxy_GraberApp')
logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')

tempproxy=[]
proxyinb=[]
errorHMN=0
urlAPI=os.environ.get('api_host')

def checkproxyinbase(ip, port):
    for i in range(len(proxyinb)-1):
        if proxyinb[i]['ip']==ip:
            if int(proxyinb[i]['port'])==int(port):
                return True
    return False


def sendmysqlnew(proxy):
    global proxyinb, tempproxy
    stime=time.time()
    goodproxy=[]
    for i in range(len(proxy)-1):
        if checkproxyinbase(proxy[i]['ip'],proxy[i]['port'])==False:
            tproxy=[proxy[i]['ip'], proxy[i]['port']]
            goodproxy.append(tproxy)
            proxyinb.append(proxy[i])
    log.info('Проверены прокси за: %sc.'%(time.time()-stime))
    stime=time.time()
    for i in range(len(goodproxy)-1):
        error=1
        while error==1:
            try:
                api_post = f"{urlAPI}?ip={goodproxy[i][0]}&port={goodproxy[i][1]}"
                response = requests.post(api_post)
                if response.status_code==201:
                    error=0
            except:
                log.error('Чёт не получилось отправить прокси попробуем ещё')
                time.sleep(5)
    log.info('Отправлены прокси за: %sс. %sшт. новых прокси'%(time.time()-stime,len(goodproxy)))
    return


def add(proxy):
    global tempproxy
    for i in range(len(proxy)-1):
        tproxy={}
        tproxy['ip']=proxy[i]['ip']
        tproxy['port']=proxy[i]['port']
        tempproxy.append(tproxy)

urls=['https://www.socks-proxy.net/', 'https://free-proxy-list.net/',
        'https://www.sslproxies.org/', 'https://free-proxy-list.net/anonymous-proxy.html',
        'https://www.us-proxy.org/', 'https://free-proxy-list.net/uk-proxy.html'
        ]
def fiveminut():
    for i in list(urls):
        try:
            add(proxyGraber.main(i))
        except: pass
    try:    
        add(GraberText.main())
    except: pass

def threehour():
    global errorHMN
    if errorHMN<=10:
        try:
            add(HideMyName.main())
        except:
            log.error('Чёт не получилось украсть с ХМН. Но мы попробуем ещё :)')
            errorHMN+=1
    return


def main():
    fiveminut()
    threehour()
    time3H=time.time()
    time5M=time.time()
    while True:
        tempt=time.time()
        if tempt-time5M>=300:
            fiveminut()
            time5M=time.time()
            log.info('Время работы грабера 5минтки: %s сек.'%(time5M-tempt))
        if tempt-time3H>=10800:
            threehour()
            time3H=time.time()
        if len(tempproxy)>0:
            sendmysqlnew(tempproxy)
        time.sleep(60)

main()
