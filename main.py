import requests
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from bs4 import BeautifulSoup as bs
import csv
import random
import time
import datetime
import sys
import os
import matplotlib.pyplot as plt

headers ={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
          'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

name = input('Введите вакансию : ')
base_url = "https://hh.kz/search/vacancy?L_is_autosearch=false&area=40&clusters=true&currency_code=KZT&enable_snippets=true&text={}&page=0".format(name)

t1= time.time()


def hh_parser(base_url,headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, 'lxml')
    try:
        pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
        count = int(pagination[-1].text)
    except:
        count =0
    for item in range(1,count+1):
        url = base_url[:-1] + format(item)
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            text = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            region = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            date = div.find('span', class_={'vacancy-serp-item__publication-date'}).text
            try:
                money = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except:
                money = None
            jobs.append(
                {
                    'title': title,
                    'href': href,
                    'company': company,
                    'text': text,
                    'money':money,
                    'region':region,
                    'date':date
                }
            )
    df = pd.DataFrame(jobs)
    df.to_excel('hh/{}-{} г.{}'.format(name,datetime.date.today(),'xlsx'),index=None)
    print(df['region'].value_counts().plot(kind='barh',color='red'))
    plt.show()
    return jobs

hh_parser(base_url,headers)
t2=time.time() - t1
print('Завершено за % s'%(t2))
time.sleep(5)
sys.exit()


