#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import TbBanner
from sqlalchemy import desc, and_
import logging
from flask import g
from application import quote_reids_store
from utils.util import pubtool

logger = logging.getLogger("sql")


class Banner:
	@staticmethod
	def get_banner_list(banner_type=None, index=1, limit=10):
		try:
			query = TbBanner.query
			if banner_type is not None:
				query = query.filter_by(btype=banner_type)
			totalobj = query
			query = query.order_by(TbBanner.btype).order_by(desc(TbBanner.weight)).paginate(index, limit).items
			return query, totalobj.count()
		except Exception as error:
			print error
			logger.info("获取banner列表出错 err={error}".format(error=error))
			return 0

	@staticmethod
	def get_banner_list_total(banner_type=None):
		try:
			query = TbBanner.query
			if banner_type is not None:
				query = query.filter_by(btype=banner_type)
			totalobj = query
			return totalobj.count()
		except Exception as error:
			print error
			logger.info("获取banner列表出错 err={error}".format(error=error))
			return 0

	@staticmethod
	def banner_list_data(banner_type=None, index=1, limit=10):
		try:
			query = TbBanner.query
			if banner_type is not None:
				query = query.filter_by(btype=banner_type)
			query = query.order_by(TbBanner.btype).order_by(desc(TbBanner.weight)).paginate(index, limit).items
			return query
		except Exception as error:
			print error
			logger.info("获取banner列表出错 err={error}".format(error=error))
			return []

	@staticmethod
	def update_banner_status(id, status):
		''' 修改banner的状态 '''
		try:
			with app.app_context():
				banner_obj = TbBanner.query.filter(TbBanner.id == id).first()
				banner_obj.status = int(status)
				db.session.commit()
				pubtool.del_mobile_client_redis_banner()
				return 1
		except Exception as e:
			print e
			logger.info('修改banner的状态出错')
			return e

	@staticmethod
	def del_banner(banner_id):
		try:
			with app.app_context():
				db.session.query(TbBanner).filter(TbBanner.id == banner_id).delete()
				db.session.commit()
				pubtool.del_mobile_client_redis_banner()
			return 0
		except Exception as error:
			print error
			logger.info("删除banner出错 err={error}".format(error=error))
			return error

	@staticmethod
	def update_banner_weight(weight_list=None):
		try:
			with app.app_context():
				for entry in weight_list:
					banner = TbBanner.query.filter_by(id=entry["_id"]).first()
					banner.weight = int(entry["weight"])
				db.session.commit()
				pubtool.del_mobile_client_redis_banner()
			return 0
		except Exception as error:
			print error
			logger.info("修改banner的权重出错 err={error}".format(error=error))
			return error

	@staticmethod
	def get_banner_weight(btype=0):
		try:
			bannerobj = TbBanner.query.filter_by(btype=btype).order_by(desc(TbBanner.weight)).first()
			return bannerobj.weight if bannerobj else 0
		except Exception as error:
			print error
			logger.info("获取banner权重出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def get_banner_details(banner_id=None):
		if not banner_id:
			return {}
		try:
			bannerobj = TbBanner.query.filter_by(id=banner_id).first()
			return bannerobj
		except Exception as error:
			print error
			logger.info("获取banner详情出错 err={error}".format(error=error))
			return {}

	@staticmethod
	def add_banner(banner_url="", btype=0, jtype=0, jump_url="", weight=0, cur_time=0,jid=0,version_type=0,status=1):
		try:
			with app.app_context():
				banner = TbBanner(btype=btype, jtype=jtype, url=jump_url, pic=banner_url, weight=weight,
				                  created_time=cur_time,last_time=cur_time, status=status,jid=jid)
				db.session.add(banner)
				db.session.commit()
				pubtool.del_mobile_client_redis_banner()
			return 0
		except Exception as error:
			print error
			logger.info("新增banner出错 err={error}".format(error=error))
			return error


	@staticmethod
	def edit_banner(banner_url="", btype=0, jtype=0, jump_url="", cur_time=0,banner_id=0,status=1,jid=0):
		try:
			with app.app_context():
				user_role = TbBanner.query.filter_by(id=banner_id).first()
				user_role.pic = banner_url
				user_role.btype = btype
				user_role.jtype = jtype
				user_role.url = jump_url
				user_role.status = status
				user_role.last_time = cur_time
				user_role.jid = jid
				db.session.commit()
				pubtool.del_mobile_client_redis_banner()
			return 0
		except Exception as error:
			print error
			logger.info("编辑banner出错 err={error}".format(error=error))
			return error