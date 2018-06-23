#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import os
class Config():
	# 启动
	HOST = "0.0.0.0"
	PORT = 5001
	DEBUG = False

	SQLALCHEMY_POOL_TIMEOUT = 15
	SQLALCHEMY_POOL_SIZE = 6
	SQLALCHEMY_POOL_RECYCLE = 180

	# redis
	REDIS_URL = "redis://localhost:6379/0"
	# 数据库
	DB = {

	}
	#七牛配置
	QINIU = {
		"access_key":"B_g75tCn6AMDtd8FLkQNbCftre4MOwAMSeYC46za",
		"secret_key":"RMOpLjlN1aLWjq2ZUSeNQNSYUTp07umQBU2HQKqz",
		"bucket_name":"if-will",
		"qn_domain_name":"http://7u2mbm.com1.z0.glb.clouddn.com/"
	}
	template_folder = 'templates'
	basedir = os.path.abspath(os.path.dirname(__file__))
	STATIC_PATH = os.path.join(os.getcwd(), "static")

class TestingConfig(Config):
	# 启动
	HOST = "0.0.0.0"
	PORT = 5001
	DEBUG = False

	# PYTHON reids
	PYTHON_REDIS_URL = "redis://127.0.0.1:6379/0"
	# 行情 备份 redis
	REDIS_QUOTE_BACKUP_URL = "redis://127.0.0.1:6379/0"
	# 后台数据库地址
	SQLALCHEMY_DATABASE_URI = "mysql://root:000000@127.0.0.1:3306/earfin"
	# SQLALCHEMY_DATABASE_URI = "mysql://root:000000@114.24.72.141:3306/earfin"
	# 图片服务器
	IMAGE_DIR = "/Users/wangranming/share/images"
	MESSAGE_SEVER = "http://127.0.0.1:8222"
	PYTHON_SERVER = "http://127.0.0.1:8888"

	SQLALCHEMY_BINDS = {
		'backendrdb': "mysql://root:000000@127.0.0.1:3306/earfin",#后台读库
		# 'backendrdb': "mysql://root:000000@114.24.72.141:3306/earfin",#后台读库
	}
	# SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True





class ProductConfig(Config):
	# 启动
	HOST = "0.0.0.0"
	PORT = 5001
	DEBUG = False
	# PYTHON reids
	PYTHON_REDIS_URL = "redis://192.168.6.78:6379/0"
	# 后台数据库地址
	SQLALCHEMY_DATABASE_URI = "mysql://iterduo:iterduo@114.24.72.141:3306/earfin"
	# 图片服务器
	IMAGE_DIR = "/data/share/images/"
	SQLALCHEMY_BINDS = {
		'backendrdb':"mysql://iterduo:iterduo@114.24.72.141:3306/earfin"
	}
	# SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

