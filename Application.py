#encoding:utf8

import threading
import time
import requests
from bs4 import BeautifulSoup
# from model import spiderModel

class spider(object):
	def __init__(self):
		self.res = ""
		# self.chapterName = spiderModel
		pass

	@staticmethod
	def instance():
		global m_instance
		try:
			m_instance
		except:
			m_instance = spider()
		return m_instance


	def dataget(self):
		url = "http://book.zongheng.com/book/683061.html"
		self.res = requests.get(url).text
		# print(self.res)

		self.dealxpath()

	def dealxpath(self):
		if self.res == "":
			return
		soup = BeautifulSoup(self.res, "html5lib")
		chapter_class = soup.find(attrs={'class':"chap"})
		chapter_str = ""
		for s in chapter_class:
			# print(s.name)
			if s.name == "p":
				continue
			chapter_str += (s.string).strip()
		print(chapter_str)

		time_class = soup.find(attrs={"class":"uptime"})
		time_str = (time_class.text).split("前")[0].strip()
		time_num = ""
		time_date = ""
		dict_time = {"小时":"小时", "分钟":"分钟", "秒":"秒"}
		for d in dict_time:
			if d in time_str:
				time_date = dict_time[d]
				break

		for ch in time_str:
			if ch >= "0" and ch <="9":
				time_num += ch

		if(time_num == ""):
			time_num = -1
		else:
			time_num = int(time_num)

		print(time_num, time_date)


def run():
	print("time:%s" % time.time())
	spider().instance().dataget()
	global timer
	timer = threading.Timer(120, run)
	timer.start()
	pass

if __name__ == "__main__":
	timer = threading.Timer(120, run)
	timer.start()
