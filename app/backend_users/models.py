#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, db
from dao.models import User
from sqlalchemy import desc, and_
import logging
from flask import g
from application import quote_reids_store

logger = logging.getLogger("sql")


class BackUser:
	@staticmethod
	def query_user_backend(user_name):
		"""查询用户名"""
		try:
			res = User.query.filter(and_(User.username == user_name, User.status != 3)).first()
			if res:
				return "用户名已经存在"
			return 0
		except Exception as E:
			print E
			logger.info(E)
			return str(E)

	@staticmethod
	def query_user_list(index=1, limit=10, uid=None, showall=0):
		"""用户列表"""
		try:
			query = User.query.filter(User.status != 3)
			if not showall:
				query = query.filter(User.user_created_id == uid)
			query = query.order_by(User.id)
			totalobj = query.all()
			user_list = query.paginate(index, limit).items
			return user_list, len(totalobj)
		except Exception as E:
			print E
			logger.info(E)
			return [], 0

	@staticmethod
	def query_backend_user_info(user_id):
		"""获取用户信息"""
		try:
			userobj = User.query.filter_by(id=user_id).first()
			return userobj
		except Exception as E:
			print E
			logger.info(E)
			return {}
