# 豆瓣movie 250
# encoding=utf-8
import bs4
import codecs
import os
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250'


def download_page(url: object) -> object:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.101 Safari/537.36'
    }
    data = requests.get(url, headers=header).content
    return data


# 处理html的函数
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    tag = movie_list_soup.find_all('li')
    for movie_li in tag:
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)
        print (movie_name_list)
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list


def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies = parse_html(html)
            #print(url)
            #print(movies)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


# 此处的方法 是只有执行本文件才调用main函数
if __name__=="__main__":
    main()
