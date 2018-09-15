import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def crawl_data(stock_code):
    headers = {
        'Referer': 'http://quotes.money.163.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }
    try:
        stock_code_new = ''
        if int(stock_code[0]) in [0, 2, 3, 6, 9]:
            if int(stock_code[0]) in [6, 9]:
                stock_code_new = '0' + stock_code
            elif int(stock_code[0]) in [0, 2, 3]:
                if not int(stock_code[:3]) in [201, 202, 203, 204]:
                    stock_code_new = '1' + stock_code
        if stock_code_new:
            stock_url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(stock_code)
            respones = requests.get(stock_url, headers=headers).text
            soup = bs(respones, 'lxml')
            start_time = soup.find('input', {'name': 'date_start_type'}).get('value').replace('-', '')    # 获取起始时间
            end_time = soup.find('input', {'name': 'date_end_type'}).get('value').replace('-', '')        # 获取结束时间
            download_url = "http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;".format(stock_code_new, start_time, end_time)
            data = requests.get(download_url, headers=headers)
            with open('static/stock.csv', 'wb') as f:                                 #保存数据
                for chunk in data.iter_content(chunk_size=10000):
                    if chunk:
                        f.write(chunk)
                        return True
    except:
        return False

def csv2data(stock_code):
    status = crawl_data(stock_code)
    if status:
        df = pd.read_csv('static/stock.csv', encoding='gbk', usecols=[0, 2, 3, 4, 5, 6])
        stock_name = df['名称'][0]
        del df['名称']
        header = [["<b>{}</b>".format(i)] for i in df.columns.tolist()]
        data = df.T.values.tolist()
        return data, stock_name, header
    else:
        return False, False, False

