import requests
import sqlite3

from twisted.internet import task, reactor

API_TOKEN = 'pub_1206463f27bfb7ce67ab994d34e41cc524d38'

params1 = {
    'apikey': API_TOKEN,
    'category': 'business',
    'page': '1',
    'language': 'ru'
}

data_news, data_news_for_ceo, data_news_for_accountant = [], [], []

db = sqlite3.connect('news.db')
cur = db.cursor()


def get_inside_ceo(title, content=None):
    return False


def get_inside_accountant(title, content=None):
    return False


def add_news(news: list, role: str):
    for el in news:
        cur.execute(f"insert into {role} (title, link, content, pubDate, image_url) values "
                    "(?, ?, ?, ?, ?)", (str(el['title']),
                                        str(el['link']),
                                        str(el['content']),
                                        str(el['pubDate']),
                                        str(el['image_url']),))
    db.commit()


def delete_duplication(role):
    cur.execute(f"""    delete from {role} where id not in (select * from 
    (select min(id) from news group by title) as de)""")
    db.commit()


def data_search():
    role = ''
    for el in range(1, 2):
        params1['page'] = str(el)
        res1 = requests.get('https://newsdata.io/api/1/news', params=params1)

        for j in res1.json()['results']:
            form = {
                        'title': j['title'],
                        'link': j['link'],
                        'content': j['content'],
                        'pubDate': j['pubDate'].split()[0],
                        'image_url': j['image_url']}

            if get_inside_ceo(j['title'], j['content']):
                data_news_for_ceo.append(form)

                add_news(data_news_for_ceo, 'news_for_ceo')
                data_news_for_ceo.clear()

            elif get_inside_accountant(j['title'], j['content']):
                data_news_for_accountant.append(form)

                add_news(data_news_for_accountant, 'news_for_accountant')
                data_news_for_accountant.clear()
            else:
                data_news.append(form)

                add_news(data_news, 'news')
                data_news.clear()

    delete_duplication('news')
    delete_duplication('news_for_ceo')
    delete_duplication('news_for_accountant')
    print(1)


timeout = 15
l = task.LoopingCall(data_search)
l.start(timeout)

reactor.run()
db.close()

