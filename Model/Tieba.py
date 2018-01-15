
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

from Model.postData import postdata

class TieBa(postdata):

    def __init__(self, BDUSS):
        super().__init__(BDUSS)
        self.yes = 0    #关注成功的个数
        self.no = 0     #关注失败的个数
        self.err_page_no = []   #一页一页的获取喜欢的吧列表，这是获取失败的页码
        self.likelist = []  #我喜欢的吧，类型是列表

    def attentions(self):
        with open('../lists.json', 'r') as f:
            all_like_list = json.load(f)
        pool = ThreadPool(10)
        result = pool.map(self.attention_one, all_like_list)
        pool.close()
        pool.join()

    def attention_one(self, kw):
        url = 'http://c.tieba.baidu.com/c/c/forum/like'
        tbs = self.gettbs()
        body = {
            'BDUSS': self.BDUSS,
            'fid' : self.getfid(kw),
            'tbs': self.gettbs(),
            'kw':kw,
        }
        body = self.encodeData(body)
        try:
            r = requests.post(url, headers=self.headers, data=body, timeout=10)
            res = json.loads(r.text)  # 将 json 格式转成字典
            self.yes += 1
            return True
        except:
            self.no += 1
            return False

    def deleteone(self, kw):
        url = 'http://c.tieba.baidu.com/c/c/forum/unfavo'
        body = {
            'BDUSS':self.BDUSS,
            'kw': kw,
            'fid': self.getfid(kw),
            'tbs': self.gettbs(),
        }
        body = self.encodeData(body)
        try:
            res = requests.post(url, headers=self.headers, data=body, timeout=10)
            res_dict = json.loads(res.text)
            if res_dict['error_code'] == '0':
                return True
            else:
                return False
        except:
            return  False

    def my_likes(self):
        flag = True
        i = 1
        self.likelist = []
        while(flag):
            flag = self.getlike(i)
            i += 1
        if len(self.err_page_no) > 0:
            self.re_getlike()
        return self.likelist

    def re_getlike(self):
        for i in range(0, len(self.err_page_no)):
            self.getlike(self.err_page_no[i])
        self.err_page_no = []

    def getlike(self, page_no):
        url = 'http://c.tieba.baidu.com/c/f/forum/like'
        body ={
            'BDUSS': self.BDUSS,
            '_client_version': '7',
            'page_no': str(page_no)#str()
        }
        body = self.encodeData(body)

        res = {}

        try:
            r = requests.post(url, headers=self.headers, data=body, timeout=10)
            res = json.loads(r.text)#将 json 格式转成字典
            list = res['forum_list']['non-gconforum']#字典肯定有这个键的，是普通贴吧
            for x in range(0, len(list)):
                self.likelist.append(list[x]['name'])#将一个贴吧名字存进列表
            try:
                list_guanfang = res['forum_list']['gconforum']#这个键不一定存在，是认证过的贴吧
                for x in range(0, len(list_guanfang)):
                    self.likelist.append(list_guanfang[x]['name'])
            except:
                pass
        except:
            self.err_page_no.append(page_no)#这一页获取失败
            res['has_more'] = '1'

        if res['has_more'] == '1':
            return True
        if res['has_more'] == '0':
            return False

    def profile(self):
        self.open_one_tie()
        url = "http://c.tieba.baidu.com/c/u/user/profile"
        body = {
            'BDUSS': self.BDUSS,
            'uid': self.uid,
        }
        body = self.encodeData(body)

        res = requests.post(url, headers=self.headers, data=body, timeout=10).text

        res = json.loads(res)
        self.head_url = "http://tb.himg.baidu.com/sys/portrait/item/"
        self.head_url += res['user']['portrait']
        self.download_head_img()


    def open_one_tie(self):
        url = "http://c.tieba.baidu.com/c/f/pb/page"
        body = {
            'BDUSS': self.BDUSS,
            'kz': '4072952804',
        }
        body = self.encodeData(body)
        res = requests.post(url, headers=self.headers, data=body, timeout=10).text
        res = json.loads(res)
        self.username = res['user']['name']
        self.uid = str(res['user']['id'])

    def download_head_img(self):
        res = requests.get(self.head_url)
        if res.status_code == 200:
            open('./head_img.jpg', 'wb').write(res.content)