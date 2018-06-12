#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import TbRecommendFixed
import time
import logging

logger = logging.getLogger("sql")


class NewsRecommend:
	@staticmethod
	def get_news_recommend_fixed(news_id=None):
		if not news_id:
			return []
		try:
			recommend = TbRecommendFixed.query.filter_by(news_id=news_id)
			r_list = [r.recommend_news_id for r in recommend]
			return r_list
		except Exception as error:
			print error
			logger.info("获取推荐列表出错 err={error}".format(error=error))
			return []

	@staticmethod
	def update_news_recommend(news_id,mult):
		"""更新推荐"""
		try:
			with app.app_context():
				if mult:
					db.session.query(TbRecommendFixed).filter(TbRecommendFixed.news_id == news_id).delete()
					db.session.commit()
					add_list = [TbRecommendFixed(news_id=news_id, recommend_news_id=int(_id),status=1,weight=0) for _id in mult]
					db.session.add_all(add_list)
					db.session.commit()
			return 0
		except Exception as E:
			print E
			logger.info(E)
			return str(E)
