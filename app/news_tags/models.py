#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import TbTags, TbTagsRelation
import time
import logging

logger = logging.getLogger("sql")


class NewsTags:
	@staticmethod
	def get_news_tags(news_id=None):
		if not news_id:
			return []
		try:
			tags_ids = TbTagsRelation.query.filter_by(r_id=news_id).filter_by(ptype=0)
			r_list = [r.tag_id for r in tags_ids]
			tagslist = TbTags.query.filter(TbTags.id.in_(r_list)).filter_by(ptype=0)
			news_tags = [t.name for t in tagslist]
			return news_tags
		except Exception as error:
			print error
			logger.info("获取标签列表出错 err={error}".format(error=error))
			return []

	@staticmethod
	def save_news_tags(news_id, tags_arr):
		"""保存新闻标签"""
		try:
			with app.app_context():
				if tags_arr:
					tags_list = []
					for tag_name in tags_arr:
						tag = TbTags.query.filter_by(name=tag_name).filter_by(ptype=0).first()
						if tag:
							tags_list.append(tag.id)
						else:
							add_tag = TbTags(name=tag_name, ptype=0)
							db.session.add(add_tag)
							db.session.commit()
							db.session.flush()
							tag_id = add_tag.id
							tags_list.append(tag_id)
					"""删除原有的"""
					db.session.query(TbTagsRelation).filter(TbTagsRelation.r_id == news_id).filter(
						TbTagsRelation.ptype == 0).delete()
					for t_id in tags_list:
						relation = TbTagsRelation(r_id=news_id,tag_id=t_id,ptype=0)
						db.session.add(relation)
					db.session.commit()
			return 0
		except Exception as E:
			print E
			logger.info(E)
			return str(E)