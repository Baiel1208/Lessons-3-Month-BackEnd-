from bs4 import BeautifulSoup
import requests

# url = "https://akipress.org/"
# response = requests.get(url)
# print(response)


# soup = BeautifulSoup(response.text)
# print(soup)
# news = soup.find_all('a',class_='newslink')
# j = 0
# for n in news:
#     j += 1
#     with open('news.text' ,'+a', encoding='utf-8') as f:
#         f.write(f'{j} {n.text}\n')
    # print(f'{n.text}\n')

def parsing_currency():
    url = 'https://www.nbkr.kg/index.jps?lang=Rus'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    currency = soup.find_all('td',class_='exrate')
    for usd in currency:
        # print(f' dollar {usd.text}')
        print(usd)