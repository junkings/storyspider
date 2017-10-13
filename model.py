#encoding:utf8
import sqlite3
import os

base_path = os.getcwd()

class spiderModel(object):

	def __init__(self, dbfile, tabledesc):
		self.tablename = tabledesc[0]
		self.tablefield = tabledesc[1]
		self.dbfile = dbfile

	def createDB(self):
		createlist = ["create table if not exists ", self.tablename, "(id integer primary key autoincrement, ", self.tablefield, ")"]
		createsql = "".join(createlist)
		self.conn = sqlite3.connect(self.dbfile)
		self.conn.isolation_level = None  #?
		print(createsql)
		self.conn.execute(createsql)

	def execDB(self, execsql):
		self.conn.execute(execsql)
		self.conn.commit()
		return

	def getResult(self, selectsql):
		self.cur = self.conn.cursor()
		self.cur.execute(selectsql)
		self.res = self.cur.fetchall()
		return self.res

	def getCount(self):
		return len(self.res)

	def closeDB(self):
		# self.cur.close()
		self.conn.close()

if __name__ == "__main__":
	dbfile =  base_path + r'\spider.db'
	tabledesc = ("storyN", "chatper varchar(128), storyname varchar(128)")
	# insertsql = "insert into storyN(chatper, storyname) values ('卷3', '大明春色')"
	# selectsql = "select * from storyN order by id desc "

	dbd = spiderModel(dbfile, tabledesc)
	dbd.createDB()
	# dbd.execDB(insertsql)
	# res = dbd.getResult(selectsql)
	# rows = dbd.getCount()
	dbd.closeDB()

	# for line in res:
	# 	for col in line:
	# 		print(col)
