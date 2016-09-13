#第一个爬虫
import urllib.request
res = urllib.request.urlopen('http://movie.douban.com/top250')
ret = res.read()
print (ret)