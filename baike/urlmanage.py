import pickle
import hashlib
class urlmanage(object):
	def __init__(self):
		self.new_urls = self.load_progress('new_urls.txt')
		self.old_urls = self.load_progress('old_urls.txt')

	def has_new_url(self):
		return self.new_urls_size() != 0

	def get_new_url(self):
		new_url = self.new_urls.pop()
		m = hashlib.md5()
		m.update(new_url.encode('utf-8'))
		self.old_urls_add(new_url)
		self.old_urls.add(m.hexdigest()[8:-8])
		return new_url

	def new_urls_add(self,url):
		if url is None:
			return None
		m = hashlib.md5()
		m.update(url.encode('utf-8'))
		url_md5 = m.hexdigest()[8:-8]
		if url not in self.new_urls and url_md5 not in self.old_urls:
			self.new_urls.add(url)

	def old_urls_add(self,url):
		if url is None:
			return None
		self.old_urls.add(url)

	def new_urls_size(self):
		return len(self.new_urls)

	def old_urls_size(self):
		return len(self.old_urls)

	def save_progress(self,path,date):
		with open(path,'wab') as f:
			pickle.dump(date,f)

	def load_progress(self,path):
		print('[+] 从文件载入进度: %s'%path)
		try:
			with open(path,'rb') as f:
				tmp = pickle.load(f)
				return tmp
		except:
			with open(path,'w') as f:
				pass
			print('[!] 无进度文件，创建文件：%s'%path)
		return set()

