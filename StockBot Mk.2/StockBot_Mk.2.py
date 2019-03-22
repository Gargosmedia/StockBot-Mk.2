'''
PLAN: 
    0. Input initial investment
    1. Get data from finviz screener with my params
    2. Get first 10 companies
    3. Go through application checklist for the 10
    4. Allocate money for those passing
    5. Save their prices and amount of shares bought 
    6. Loop checking their price with threshold
    7. "Sell" if past threshold
    8. Buy new ones with money gained

    Extra: 
        1. Setup disk bot for monitoring
        
'''

from bs4 import BeautifulSoup
import urllib2
import time

portfolio={}
money_p=10000
top_limit=1
bot_limit=-5
change_p=0
screener_url = 'https://finviz.com/screener.ashx?v=111&f=sh_curvol_o500,sh_price_o15,ta_highlow50d_b15h,ta_highlow52w_b20h&ft=4&o=-volume'


def main():
    global screener_url
    global money_p
    global change_p
    current_top=[]

    print "Stage 0 - Reading saved portfolio ..." 
    try:
        read_portfolio()
    except:

        
        while (len(current_top)<1):
            print "Stage 1 - Searching ..."
            current_top = parse_screener(screener_url, 1)
            

        print "Stage 2 - Buying..."
        buy(current_top)


    print "Stage 3 - Looping ..."
    while True:
        check()
        print "\n +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n"
        print "Money = " + str(money_p) + " | Change = " + str(change_p)
        print "\n +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ \n"

    
    return True


def parse_screener(url, use):
    dict={}

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = { 'User-Agent' : user_agent }
    data=""

    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    page = response.read()

    #print page
    soup = BeautifulSoup(page, 'html.parser')
    

    if (use == 1):

        for line in soup.findAll('tr',attrs={"class":"table-dark-row-cp"}):
        
            #print line
            list_attrs = line.findAll('a', attrs={"class":"screener-link"})
            l_a=[]
            for value in line.findAll('a', attrs={"class":"screener-link"}):
            
                l_a.append(value.getText().encode("utf-8"))

            #print l_a
        
            name = line.find('a', attrs={"class":"screener-link-primary"}).getText().encode("utf-8")

            full_name = l_a.pop(1)

            dict[name]=l_a

        return dict

    elif (use == 2):
        lines = soup.findAll('tr',attrs={"class":"table-dark-row"})
        fields = lines[10].findAll('b')
        price=fields[5].getText()


        return price



def buy(top_dict):
    global money_p
    global portfolio
    applicable=[]
   

    for stock, stock_attrs in top_dict.items():
        price = float(stock_attrs[6])
        if (price > 10) & (price < 2000):
            
            if stock not in portfolio:
                applicable.append(stock)
            
            else:
                pass
        else:
            pass

    #if money_p > 5000:
   #     print "Money > 5000"
    budget=round(float(money_p/len(applicable)),2) 
   # elif money_p > 100:
   #     print "100 < Money < 5000"
   #     budget=money_p
   # else:
   #     print "0 < Money < 100"
   #     budget=0

    for stock in applicable:
        attrs=top_dict[stock]
        
        price=float(attrs[6])


        if budget > price:
 
            shares=int(budget/price)
            
            #print "budget>price"
            #print budget

            print "BUYING " + str(stock) + " | Shares: " + str(shares)


            portfolio[stock]= ["Price: ", price], ["Shares bought: ", shares]
        
            money_p-=shares*price
        else:
            print "budget<price"
            pass

    save_portfolio()
    return True


def print_dict(dict):
    for key, value in dict.items():
        print key, ": ", value
    return True

def save_portfolio():
    global portfolio
    global money_p
    global change_p

    f=open("portfolio.txt", "w+")
    f.write(str(portfolio) + "/|/" + str(money_p) + "/|/" + str(change_p))


    f.close() 

def read_portfolio():
    global portfolio
    global money_p
    global change_p

    f = open("portfolio.txt", "r")

    gather=f.read().split("/|/")

    portfolio = eval(gather[0])
    money_p=eval(gather[1])
    change_p=eval(gather[2])
    
    return True



def check():
    global top_limit, bot_limit
    global portfolio

    CinS=0


    for ticker, attrs in portfolio.items():

        url='https://finviz.com/quote.ashx?t=' + str(ticker)

        new_price = float(parse_screener(url, 2))

        old_price = float(attrs[0][1])


        change = (1-round(old_price/new_price, 4)) * 100

        share_amount = int(portfolio[ticker][1][1])

        CinS+=(new_price-old_price)*share_amount




        print  (str(ticker) + " | Bought: " + str(old_price) + " New: " + str(new_price) + " | Perc: " + str(change) + '%')


        if (change > float(top_limit) or change < float(bot_limit)):

            sell(ticker, new_price, old_price)

            buy(parse_screener(screener_url, 1))

    print "\nChange in Stocks: ", CinS

    return True
    
def sell(ticker, new_price, old_price):
    global money_p
    global change_p
    global portfolio

    print "Selling " + str(ticker)
    

    share_amount = int(portfolio[ticker][1][1])

    result = (new_price*share_amount) - (old_price*share_amount) 
    change_p+=result


    money_p+=(share_amount*new_price)

    portfolio.pop(ticker)


    print "Result: " + str(round(result,2))
    print "Current Money " + str(money_p)
    print " TOTAL CHANGE => " + str(change_p)

    save_portfolio()
    return True
    

if __name__ == '__main__':    
    main()
