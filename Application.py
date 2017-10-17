#encoding:utf8

import threading
import time
import requests
from bs4 import BeautifulSoup
from model import spiderModel, dbfile, tabledesc
from mailinter import Mail

class spider(object):
	def __init__(self, story=None):
		self.res = ""
		self.model = spiderModel.instansce(dbfile, tabledesc)

		if story == None:
			self.story = {"大明春色":"http://book.zongheng.com/book/683061.html"}
		else:
			self.story = story

		self.get_chapname()
		self.Mail = Mail()

	@staticmethod
	def instance(story=None):
		global m_instance
		try:
			m_instance
		except:
			m_instance = spider(story)
		return m_instance

	def get_chapname(self):
		if not hasattr(self, "chaptername"):
			self.chaptername = dict()
		for storyName in self.story.keys():
			self.selectsql = "select chatper from storyN where storyname = '%s' order by id desc " % storyName

			self.model.connectDB()
			self.model.getResult(self.selectsql)

			self.chaptername[storyName] = self.model.getChapterName()
			self.model.closeDB()
			print("the New chapter name", self.chaptername[storyName], storyName)

	def insert_chapname(self, name, storyname):
		self.insertsql = "insert into storyN(chatper, storyname) values ('%s', '%s')" %(name, storyname)
		self.model.connectDB()
		self.model.execDB(self.insertsql)


	def dataget(self):
		for storyName in self.story:
			url = self.story[storyName]  #大明春色
			# 处理网络异常情况
			try:
				ir = requests.get(url)
			except Exception as e:
				print(e)
				return
			if ir.status_code == 200:
				self.res = ir.text
				self.dealxpath(storyName)
			time.sleep(3)
		# print(self.res)



	def dealxpath(self, storyName):
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

		if chapter_str != self.chaptername[storyName]:
			self.insert_chapname(chapter_str, storyName)
			self.chaptername[storyName] = chapter_str

			self.Mail.content(storyName+"更新： " + self.chaptername[storyName])
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
	spider.instance(story).dataget()
	global timer
	timer = threading.Timer(360, run)
	timer.start()
	pass

story = {"大明春色": "http://book.zongheng.com/book/683061.html", "永夜君王":"http://book.zongheng.com/book/342974.html"}

if __name__ == "__main__":
	spider.instance(story).dataget()
	timer = threading.Timer(360, run)
	timer.start()
	# spider.instance()
