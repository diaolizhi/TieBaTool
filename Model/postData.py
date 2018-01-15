import requests
import hashlib
import json


class postdata(object):

    def __init__(self, BDUSS):
        self.BDUSS = BDUSS  #BDUSS
        self.headers = {'Cookie':'BDUSS='+self.BDUSS}   #请求头

    def encodeData(self, data):
        SIGN_KEY = 'tiebaclient!!!'
        s = ''
        keys = data.keys()
        for i in sorted(keys):
            s += i + '=' + data[i]
        sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
        data.update({'sign': str(sign)})
        return data

    def getfid(self, kw):
        try:
            fid_url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname=' + kw
            fid = requests.get(fid_url, headers=self.headers, timeout=10).text
            fid = json.loads(fid)
            fid = fid['data']['fid']
            return str(fid)
        except:
            return '1640254'

    def gettbs(self):
        try:
            url = 'http://tieba.baidu.com/dc/common/tbs'
            tbs = requests.get(url, headers=self.headers, timeout=10).text
            tbs = json.loads(tbs)
            return str(tbs['tbs'])
        except:
            return '09a6a5f9f49e01571515644270'