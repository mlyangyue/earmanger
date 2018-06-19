#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
from flask.ext.login import UserMixin
from app import db
from application import python_redis_store
import json

"""用户权限"""

# class SysElement(db.Model):
#     __tablename__ = "sys_element"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     father_id = db.Column(db.Integer)
#     name = db.Column(db.VARCHAR(45))
#     remark = db.Column(db.VARCHAR(45))
#     etype = db.Column(db.Integer)
#
#
# class SysRoleElement(db.Model):
#     __tablename__ = "sys_role_element"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     role_id = db.Column(db.Integer)
#     element_id = db.Column(db.Integer)
#
#
# class SysRole(db.Model):
#     __tablename__ = "sys_role"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     rolename = db.Column(db.VARCHAR(45))
#     remark = db.Column(db.VARCHAR(45))
#     status = db.Column(db.Integer, default=1)
#     user_created_id = db.Column(db.VARCHAR(4))
#
#
# class SysUserRole(db.Model):
#     __tablename__ = "sys_user_role"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer)
#     role_id = db.Column(db.Integer)


"""用户"""


class User(db.Model, UserMixin):
	__tablename__ = "sys_user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.VARCHAR(45), unique=True)
	realname = db.Column(db.VARCHAR(45), unique=True)
	password = db.Column(db.VARCHAR(45))
	status = db.Column(db.Integer, default=1)
	user_created_id = db.Column(db.VARCHAR(4))
	showall = db.Column(db.Integer, default=0)

	def get_permission(self):
		_list = []
		return _list


class TbBanner(db.Model):
	__tablename__ = "tb_banner"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	pic = db.Column(db.VARCHAR(150))
	url = db.Column(db.VARCHAR(200))
	btype = db.Column(db.Integer)
	weight = db.Column(db.Integer)
	jtype = db.Column(db.Integer)
	status = db.Column(db.Integer)
	created_time = db.Column(db.Integer)
	last_time = db.Column(db.Integer)
	jid = db.Column(db.Integer)


class TbNews(db.Model):
	__tablename__ = "tb_news"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.VARCHAR(200))
	subtitle = db.Column(db.VARCHAR(150))
	tdate = db.Column(db.Integer)
	desc = db.Column(db.VARCHAR(200))
	content = db.Column(db.Text)
	author = db.Column(db.VARCHAR(45))
	read_num = db.Column(db.Integer)
	weight = db.Column(db.Integer)
	status = db.Column(db.Integer)
	real_read = db.Column(db.Integer)
	small_pic = db.Column(db.VARCHAR(150))
	created_time = db.Column(db.Integer)
	last_time = db.Column(db.Integer)
	pub_time = db.Column(db.Integer)
	details_url = db.Column(db.VARCHAR(150))


class TbRecommendFixed(db.Model):
	__tablename__ = "tb_recommend_fixed"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	news_id = db.Column(db.Integer)
	recommend_news_id = db.Column(db.Integer)
	status = db.Column(db.Integer)
	weight = db.Column(db.Integer)


class TbFastNews(db.Model):
	__tablename__ = "tb_fast_news"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	tdate = db.Column(db.Integer)
	title = db.Column(db.VARCHAR(200))
	subtitle = db.Column(db.VARCHAR(150))
	desc = db.Column(db.VARCHAR(200))
	content = db.Column(db.Text)
	author = db.Column(db.VARCHAR(45))
	weight = db.Column(db.Integer)
	status = db.Column(db.Integer)
	created_time = db.Column(db.Integer)
	last_time = db.Column(db.Integer)
	pub_time = db.Column(db.Integer, default=0)
	share_count = db.Column(db.Integer, default=0)


class TbTags(db.Model):
	__tablename__ = "tb_tags"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.VARCHAR(45))
	ptype = db.Column(db.Integer)

class TbTagsRelation(db.Model):
	__tablename__ = "tb_tag_relation"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	r_id = db.Column(db.Integer)
	tag_id = db.Column(db.Integer)
	ptype = db.Column(db.Integer)

