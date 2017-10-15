#encoding:utf8

import threading
import time
import requests
from bs4 import BeautifulSoup
from model import spiderModel, dbfile, tabledesc
from mailinter import Mail
class spider(object):
	def __init__(self):
		self.res = ""
		self.model = spiderModel.instansce(dbfile, tabledesc)
		self.get_chapname()

		self.Mail = Mail()

		pass

	@staticmethod
	def instance():
		global m_instance
		try:
			m_instance
		except:
			m_instance = spider()
		return m_instance

	def get_chapname(self):
		self.selectsql = "select chatper from storyN order by id desc "

		self.model.connectDB()
		self.model.getResult(self.selectsql)

		self.chaptername = self.model.getChapterName()
		self.model.closeDB()
		print "the New chapter name", self.chaptername

	def insert_chapname(self, name):
		self.insertsql = "insert into storyN(chatper, storyname) values ('%s', '大明春色')" %name
		self.model.connectDB()
		self.model.execDB(self.insertsql)


	def dataget(self):
		url = "http://book.zongheng.com/book/683061.html"
		# 处理网络异常情况
		try:
			ir = requests.get(url)
		except Exception as e:
			print e
			return
		if ir.status_code == 200:
			self.res = ir.text
			self.dealxpath()
		# print(self.res)



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
		# chapter_str = chapter_str.rstrip('\n')
		# print(chapter_str)

		if chapter_str != self.chaptername:
			self.insert_chapname(chapter_str)
			self.chaptername = chapter_str

			self.Mail.content("大明春色更新： " + self.chaptername)
			self.Mail.send()

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
	spider.instance().dataget()
	global timer
	timer = threading.Timer(360, run)
	timer.start()
	pass

if __name__ == "__main__":
	spider.instance().dataget()
	timer = threading.Timer(360, run)
	timer.start()
	# spider.instance()
