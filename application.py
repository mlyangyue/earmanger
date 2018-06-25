#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

import os
from redis import StrictRedis
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from cores.db import DB
from sqlalchemy import create_engine
from sqlalchemy.orm import *
from utils.qiniuclient import QiNiuClient
import contextlib
import random

db = DB()
db_manager = 0
redis_store = 0
python_redis_store = 0
quote_reids_store = 0
quote_backup_redis_store = 0
qn = QiNiuClient()

class CreateApp(Flask):
	def __init__(self, conf_path):
		super(CreateApp, self).__init__(__name__)
		self.config.from_object(conf_path)
		self.init_app()
		self.init_db(self.config['SQLALCHEMY_BINDS'])
		_dir = os.path.dirname(os.path.abspath(__file__))
		self.init_log("sql", _dir + "/log/sql", "MIDNIGHT")
		self.init_log("views", _dir + "/log/views", "MIDNIGHT")
		self.init_log("login", _dir + "/log/login", "MIDNIGHT")
		self.init_console(_dir + "/log/console")

	def init_app(self):
		global redis_store
		global python_redis_store
		global quote_reids_store
		global quote_backup_redis_store
		redis_store = FlaskRedis(self,config_prefix="REDIS")
		redis_store.init_app(self)
		python_redis_store = FlaskRedis(self,config_prefix="PYTHON_REDIS")
		python_redis_store.init_app(self)
		quote_reids_store = FlaskRedis(self,config_prefix="REDIS_QUOTE")
		quote_reids_store.init_app(self)
		quote_backup_redis_store = FlaskRedis(self, config_prefix='REDIS_QUOTE_BACKUP')
		quote_backup_redis_store.init_app(self)
		qn.init_app(self)
		# db.init_app(self)

	def init_db(self,db_config):
		global db_manager
		print 'init_db'
		db_manager = DBManager(db_config)

	def init_log(self, loggerName, filename, during, interval=1):
		import logging.handlers
		import logging
		from utils.util import pubtool
		print "logpath",loggerName
		pubtool.mkdir(loggerName)
		log = logging.getLogger(loggerName)

		fileTimeHandler = logging.handlers.TimedRotatingFileHandler(filename, during, interval, backupCount=10)
		formatter = logging.Formatter(
			'%(name)-12s %(asctime)s level-%(levelname)-8s thread-%(thread)-8d [%(filename)s:%(lineno)s] %(message)s')  # 每行日志的前缀设置
		logging.basicConfig(level=logging.INFO)
		fileTimeHandler.setFormatter(formatter)
		log.addHandler(fileTimeHandler)

	def init_console(self, file_path):
		import logging
		fileStreamHandler = logging.StreamHandler(file_path)  # sys.stderr
		log = logging.getLogger("console")
		formatter = logging.Formatter(
			'%(name)-12s %(asctime)s level-%(levelname)-8s thread-%(thread)-8d %(message)s')  # 每行日志的前缀设置

		fileStreamHandler.setFormatter(formatter)
		log.addHandler(fileStreamHandler)

class DBManager(object):
	def __init__(self,db_settings):
		self.session_map = {}
		self.create_sessions(db_settings)


	def create_sessions(self,db_settings):

		# db_settings = {  # 为了简单，我直接把数据库的配置结构写在了这里，这个配置应该在另外的地方加载进来
		# 	'master': 'mysql://root:root@127.0.0.1:3306/testdb',
		# 	'slave': 'mysql://root:root@127.0.0.1:3306/testdb'
		# }
		for role, url in db_settings.items():
			self.session_map[role] = self.create_single_session(url)
		print self.session_map

	@classmethod
	def create_single_session(cls, url, scopefunc=None):
		engine = create_engine(url,convert_unicode=True)
		return scoped_session(
			sessionmaker(
				expire_on_commit=False,
				bind=engine,

			),
			scopefunc=scopefunc
		)

	def get_session(self, name):
		try:
			if not name:
				# 当没有提供名字时，我们默认为读请求，现在的逻辑是在当前所有的配置中随机选取一个数据库，你可以根据自己的需求来调整这里的选择逻辑
				name = random.choice(self.session_map.keys())

			return self.session_map[name]
		except KeyError:
			raise KeyError('{} not created, check your DB_SETTINGS'.format(name))
		except IndexError:
			raise IndexError('cannot get names from DB_SETTINGS')

	@contextlib.contextmanager
	def session_ctx(self, bind=None):
		DBSession = self.get_session(bind)
		session = DBSession()
		try:
			yield session
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.expunge_all()
			session.close()
