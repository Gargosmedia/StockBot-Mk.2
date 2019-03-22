
from bs4 import BeautifulSoup
import urllib2


rating=0    # 0-100


def main():

    ticker = raw_input("Ticker: ") 

    url="https://finviz.com/quote.ashx?t=" + ticker
    try:
        data=parse_screener(url)
    except:
        return False
    rsi_r=50-mapFromTo(data[1],30,70,0,50)
    print "rsi_r: " + str(rsi_r)
    volume_r=mapFromTo(data[2],0,1000000,0,30)
    print "volume_r: " + str(volume_r)
    range_r=20-mapFromTo(data[0],float(data[3][0]),float(data[3][1]),0,20)
    print "range_r: " + str(range_r)
 
    rating=round(rsi_r+volume_r+range_r)
    print "Rating: "+str(rating)

    return True


def mapFromTo(x,a,b,c,d):
   
   # x:input value; 
   # a,b:input range
   # c,d:output range
   
   y=(x-a)/(b-a)*(d-c)+c
  
   return y

def parse_screener(url):
    dict={}

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = { 'User-Agent' : user_agent }
    data=""

    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    page = response.read()

    #print page
    soup = BeautifulSoup(page, 'html.parser')
    lines = soup.findAll('tr',attrs={"class":"table-dark-row"})

    fields = lines[10].findAll('b')
    price=fields[5].getText()
  
    fields = lines[8].findAll('b')
    rsi=fields[4].getText()
    
    print "RSI: " + str(rsi)
    
    if float(rsi)<30:
        rsi=30.00+1.00
    elif float(rsi)>70:
        rsi=70.00-1.00
    

    fields = lines[11].findAll('b')
    volume=fields[4].getText()
    volume=volume.replace(',', '')
  

    fields = lines[5].findAll('b')
    range=fields[4].getText().split("-")
 

    if int(volume)>1000000:

        print "vol > 1m"
        volume=1000000

    #print(price, rsi, volume, range)
    return float(price), float(rsi), float(volume), range


while True:
    main()