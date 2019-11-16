import requests 
from bs4 import BeautifulSoup 

#read latest date from db - if empty || < latest article date -  go on reading articles 

def send_message_to_telegram(textmsg):
    url = 'https://api.telegram.org/bot<BOT-TOKEN>/sendMessage?chat_id=<PUBLIC CHANNEL ID>&text={}'.format(textmsg)
    r = requests.get(url)
    print(r)

def check_latest_article_date(soup):
    last_update = soup.select('.article > div > h3')
    return last_update[0].get('data-utc')

def persist_latest_article_date(utc_date):
    db = open("db.txt","a")
    db.write(utc_date)
    db.close()

def read_latest_date_from_db():
    all_lines = []
    db = open("db.txt","r")
    all_lines = db.readlines()
    return all_lines[-1]

URL = "https://jsfeeds.com"
r = requests.get(URL)  
soup = BeautifulSoup(r.content, 'html5lib') 

all_artile_link = soup.select('.article > div > div > div > div > div > a:nth-child(1)')
all_article_dates = soup.select('.article > div > h3')
try:
    latest_date_in_db = read_latest_date_from_db()
    print('lateset in db:',latest_date_in_db)
except FileNotFoundError as File_error :
    print(File_error)
    latest_date_in_db = 0

for article , date in zip(all_artile_link , all_article_dates):
    articles_date = int(date.get('data-utc'))
    if int(latest_date_in_db) >= articles_date:
        break
    send_message_to_telegram(URL+article.get('href'))

if int(check_latest_article_date(soup)) > int(latest_date_in_db):
    persist_latest_article_date(check_latest_article_date(soup))


