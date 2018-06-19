#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import TbFastNews
from sqlalchemy import desc, and_
import time
import logging
from flask import g
from application import quote_reids_store
from utils.util import pubtool
from configs.constants import NEWSURL

logger = logging.getLogger("sql")


class FastNews:
	@staticmethod
	def get_fast_news_list_total():
		try:
			query = TbFastNews.query
			totalobj = query
			return totalobj.count()
		except Exception as error:
			print error
			logger.info("获取fast_news列表出错 err={error}".format(error=error))
			return 0

	@staticmethod
	def fast_news_list_data(status=None, index=1, limit=10):
		try:
			query = TbFastNews.query
			if status is not None:
				query = query.filter(TbFastNews.status == status)
			query = query.order_by(desc(TbFastNews.weight)).paginate(index, limit).items
			return query
		except Exception as error:
			print error
			logger.info("获取fast_news列表出错 err={error}".format(error=error))
			return []

	@staticmethod
	def update_fast_news_status(id, status):
		''' 修改fast_news的状态 '''
		try:
			with app.app_context():
				fast_news_obj = TbFastNews.query.filter(TbFastNews.id == id).first()
				fast_news_obj.status = int(status)
				if int(status) == 1:
					fast_news_obj.pub_time = int(time.time())
				fast_news_obj.last_time = int(time.time())
				db.session.commit()
				pubtool.del_mobile_client_redis_fast_news()
				return 1
		except Exception as e:
			print e
			logger.info('修改fast_news的状态出错')
			return e

	@staticmethod
	def del_fast_news(fast_news_id):
		try:
			with app.app_context():
				db.session.query(TbFastNews).filter(TbFastNews.id == fast_news_id).delete()
				db.session.commit()
				pubtool.del_mobile_client_redis_fast_news()
			return 0
		except Exception as error:
			print error
			logger.info("删除fast_news出错 err={error}".format(error=error))
			return error

	@staticmethod
	def update_fast_news_weight(weight_list=None):
		try:
			with app.app_context():
				for entry in weight_list:
					broadcast = TbFastNews.query.filter_by(id=entry["_id"]).first()
					broadcast.weight = int(entry['weight'])
				db.session.commit()
				pubtool.del_mobile_client_redis_fast_news()
			return 0
		except Exception as e:
			print e
			logger.info('修改fast_news权重信息出错  error={error}'.format(error=e))
			return e

	@staticmethod
	def get_fast_news_details(fast_news_id=None):
		if not fast_news_id:
			return {}
		try:
			bannerobj = TbFastNews.query.filter_by(id=fast_news_id).first()
			return bannerobj
		except Exception as error:
			print error
			logger.info("获取fast_news详情出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def get_fast_news_weight():
		try:
			fast_newsobj = TbFastNews.query.order_by(desc(TbFastNews.weight)).first()
			return fast_newsobj.weight if fast_newsobj else 0
		except Exception as error:
			print error
			logger.info("获取fast_news权重出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def add_fast_news(title='', subtitle='', author='', cur_time=0, desc='', content='', weight=0, tdate=0):
		try:
			with app.app_context():
				fast_news = TbFastNews(title=title, subtitle=subtitle, author=author, created_time=cur_time, desc=desc,
				                       content=content, last_time=cur_time, weight=weight, tdate=tdate, status=0)
				db.session.add(fast_news)
				db.session.commit()
				pubtool.del_mobile_client_redis_fast_news()
			return 0
		except Exception as error:
			print error
			logger.info("新增FASTNEWS出错 err={error}".format(error=error))
			return error

	@staticmethod
	def edit_fast_news(title='', subtitle='', author='',cur_time=0, desc='', content='', tdate=0,fast_news_id=0):
		try:
			with app.app_context():
				fast_news = TbFastNews.query.filter_by(id=fast_news_id).first()
				fast_news.title = title
				fast_news.subtitle = subtitle
				fast_news.author = author
				fast_news.desc = desc
				fast_news.content = content
				fast_news.last_time = cur_time
				db.session.commit()
				pubtool.del_mobile_client_redis_fast_news()
			return 0
		except Exception as error:
			print error
			logger.info("编辑fast_news出错 err={error}".format(error=error))
			return error

