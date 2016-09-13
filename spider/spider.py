#spider
#encoding=utf8
import urllib.request
import os
import json
from bs4 import BeautifulSoup

Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}
_session = requests.session()
_session.headers.update(Default_Header) 
resourceFile = open('/root/Desktop/UserId.text','r')
resourceLines = resourceFile.readlines()
resultFollowerFile = open('/root/Desktop/userIdFollowees.text','a+')
resultFolloweeFile = open('/root/Desktop/userIdFollowers.text','a+')

BASE_URL = 'https://www.zhihu.com/'
CAPTURE_URL = BASE_URL+'captcha.gif?r=1466595391805&type=login'
PHONE_LOGIN = BASE_URL + 'login/phone_num'

def login():
    '''登录知乎'''
    username = '273861699@qq.com' #用户名
    password = '1986214000cd' #密码，注意我这里用的是手机号登录，用邮箱登录需要改一下下面登录地址
    cap_content = urllib2.urlopen(CAPTURE_URL).read()
    cap_file = open('/root/Desktop/cap.gif','wb')
    cap_file.write(cap_content)
    cap_file.close()
    captcha = raw_input('capture:')
    data = {"phone_num":username,"password":password,"captcha":captcha}
    r = _session.post(PHONE_LOGIN, data)
    print (r.json())['msg']
    
def readFollowerNumbers(followerId,followType):
    '''读取每一位用户的关注者和追随者，根据type进行判断'''
    print (followerId)
    personUrl = 'https://www.zhihu.com/people/' + followerId.strip('\n')
    xsrf =getXsrf()
    hash_id = getHashId(personUrl)
    headers = dict(Default_Header)
    headers['Referer']= personUrl + '/follow'+followType
    followerUrl = 'https://www.zhihu.com/node/ProfileFollow'+followType+'ListV2'
    params = {"offset":0,"order_by":"created","hash_id":hash_id}
    params_encode = json.dumps(params)
    data = {"method":"next","params":params_encode,'_xsrf':xsrf}
    
    signIndex = 20
    offset = 0
    while signIndex == 20:
        params['offset'] = offset
        data['params'] = json.dumps(params)
        followerUrlJSON = _session.post(followerUrl,data=data,headers = headers)
        signIndex = len((followerUrlJSON.json())['msg'])
        offset = offset + signIndex
        followerHtml =  (followerUrlJSON.json())['msg']
        for everHtml in followerHtml:
            everHtmlSoup = BeautifulSoup(everHtml)
            personId =  everHtmlSoup.a['href']
            resultFollowerFile.write(personId+'\n')
            print (personId)
            
    
def getXsrf():
    '''获取用户的xsrf这个是当前用户的'''
    soup = BeautifulSoup(_session.get(BASE_URL).content)
    _xsrf = soup.find('input',attrs={'name':'_xsrf'})['value']
    return _xsrf
    
def getHashId(personUrl):
    '''这个是需要抓取的用户的hashid，不是当前登录用户的hashid'''
    soup = BeautifulSoup(_session.get(personUrl).content)
    hashIdText = soup.find('script', attrs={'data-name': 'current_people'})
    return json.loads(hashIdText.text)[3]

def main():
    login()
    followType = input('请配置抓取类别：0-抓取关注了谁 其它-被哪些人关注')
    followType = 'ees' if followType == 0 else 'ers'
    for followerId in resourceLines:
        try:
            readFollowerNumbers(followerId,followType)
            resultFollowerFile.flush()
        except:
            pass
   
if __name__=='__main__':
    main()