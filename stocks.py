import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

#set graph style
style.use('ggplot')

#/*THIS SECTION PULLS FROM API TO GIVE DATA
#set date ranges
#start = dt.datetime(2015, 1, 1)
#end = dt.datetime.now()

#get a stock
#df = web.DataReader('TSLA', "yahoo", start, end)

#simplify the dataframe
#df.reset_index(inplace=True)
#df.set_index("Date", inplace=True)

#print(df.head())

#dataframe to a CSV
#df.to_csv('TSLA.csv')
#*////////////

#reload the data from CSV file into dataframe
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

#/*THIS SECTION PLOTS THE 100 DAY ROLLING AVG
#plot a graph
df['Adj Close'].plot()

plt.show()

#creating a 100 day rolling average of dataframe
df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
print(df.head())

#plot the average
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

#plot the close prices on top and volume on bottom
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()

#*/////////////////

#*/ S&P500 Tickers from Wikipedia
#import beautifulsoup for html parsing, pickle for saving lists, requests for Wiki source code
import bs4 as bs
import pickle
import requests

def save_sp500_tickers():
    #request source code
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    #make some soup
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    #collect the data needed
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    #using pickle to serialize our python beautifulsoup objects
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    return tickers

#SECTION BELOW USES PANDAS, WON'T WORK CORRECTLY
import datetime as dt #specifies dates for Panda
import os #checking/creating directories
import pandas_datareader.data as web

save_sp500_tickers()
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    #make directory
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers[:15]:
        #save progress
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

#get_data_from_yahoo()