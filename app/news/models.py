#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import TbNews
from sqlalchemy import desc, and_
import time
import logging
from flask import g
from utils.util import pubtool
from configs.constants import NEWSURL

logger = logging.getLogger("sql")


class News:
	@staticmethod
	def get_news_list_total():
		try:
			query = TbNews.query
			totalobj = query
			return totalobj.count()
		except Exception as error:
			print error
			logger.info("获取news列表出错 err={error}".format(error=error))
			return 0

	@staticmethod
	def news_list_data(status=None, index=1, limit=10):
		try:
			query = TbNews.query
			if status is not None:
				query = query.filter(TbNews.status == status)
			query = query.order_by(desc(TbNews.weight)).order_by(desc(TbNews.id)).paginate(index, limit).items
			return query
		except Exception as error:
			print error
			logger.info("获取news列表出错 err={error}".format(error=error))
			return []

	@staticmethod
	def update_news_status(id, status):
		''' 修改news的状态 '''
		try:
			with app.app_context():
				news_obj = TbNews.query.filter(TbNews.id == id).first()
				news_obj.status = int(status)
				if int(status)==1:
					news_obj.pub_time = int(time.time())
				news_obj.last_time = int(time.time())
				db.session.commit()
				pubtool.del_mobile_client_redis_news()
				return 1
		except Exception as e:
			print e
			logger.info('修改news的状态出错')
			return e

	@staticmethod
	def del_news(news_id):
		try:
			with app.app_context():
				db.session.query(TbNews).filter(TbNews.id == news_id).delete()
				db.session.commit()
				pubtool.del_mobile_client_redis_news()
			return 0
		except Exception as error:
			print error
			logger.info("删除news出错 err={error}".format(error=error))
			return error

	@staticmethod
	def update_news_weight(weight_list=None):
		try:
			with app.app_context():
				for entry in weight_list:
					broadcast = TbNews.query.filter_by(id=entry["_id"]).first()
					broadcast.weight = int(entry['weight'])
				db.session.commit()
				pubtool.del_mobile_client_redis_news()
			return 0
		except Exception as e:
			print e
			logger.info('修改news权重信息出错  error={error}'.format(error=e))
			return e

	@staticmethod
	def get_news_details(news_id=None):
		if not news_id:
			return {}
		try:
			newsobj = TbNews.query.filter_by(id=news_id).first()
			return newsobj
		except Exception as error:
			print error
			logger.info("获取news详情出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def get_news_weight():
		try:
			newsobj = TbNews.query.order_by(desc(TbNews.weight)).first()
			return newsobj.weight if newsobj else 0
		except Exception as error:
			print error
			logger.info("获取news权重出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def add_news(title='', subtitle='', author='', read_num=0, cur_time=0, desc='', content='', weight=0, tdate=0,
	             small_pic=''):
		try:
			with app.app_context():
				news = TbNews(title=title, subtitle=subtitle, author=author, read_num=read_num, created_time=cur_time,
				              desc=desc, content=content, last_time=cur_time, weight=weight, tdate=tdate,
				              small_pic=small_pic, status=0, real_read=0,details_url="")
				db.session.add(news)
				db.session.commit()
				db.session.flush()
				_id = news.id
				details_url = NEWSURL + str(_id)
				addnews = TbNews.query.filter_by(id=_id).first()
				addnews.details_url=details_url
				db.session.commit()
				pubtool.del_mobile_client_redis_news()
			return 0
		except Exception as error:
			print error
			logger.info("新增NEWS出错 err={error}".format(error=error))
			return error

	@staticmethod
	def edit_news(title='', subtitle='', author='', read_num=0, cur_time=0, desc='', content='', tdate=0,
	             small_pic='',news_id=0):
		try:
			with app.app_context():
				news = TbNews.query.filter_by(id=news_id).first()
				news.title=title
				news.subtitle=subtitle
				news.author=author
				news.read_num=read_num
				news.desc=desc
				news.content=content
				news.small_pic=small_pic
				news.last_time=cur_time
				db.session.commit()
				pubtool.del_mobile_client_redis_news()
			return 0
		except Exception as error:
			print error
			logger.info("编辑news出错 err={error}".format(error=error))
			return error

	@staticmethod
	def get_newslist_data(newslist,index=1,limit=10):
		"""批量获取新闻列表"""
		if not newslist:
			return []
		_news_list = [str(st) for st in newslist]
		nstr = ",".join(_news_list)
		try:
			query = TbNews.query
			query = query.filter(TbNews.id.in_(nstr))
			query = query.order_by(desc(TbNews.weight)).paginate(index, limit).items
			return query
		except Exception as error:
			print error
			logger.info("获取news列表出错 err={error}".format(error=error))
			return []