import requests
class Download(object):
    def download(self,url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        heads = {'User-Agent':user_agent}
        r = requests.get(url,headers=heads,)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
