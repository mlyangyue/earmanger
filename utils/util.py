#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from base64 import b64encode, b64decode
from configs import constants
from application import python_redis_store
import xlwt
import os


class PublicTools:
	@staticmethod
	def unicode_to_utf8(ustr=None):
		"""unicode转utf8"""
		if isinstance(ustr, unicode):
			return ustr.encode('utf-8')
		return ustr

	@staticmethod
	def utf8_to_unicode(utfstr=None):
		"""utf8转unicode"""
		if not isinstance(utfstr, unicode):
			return utfstr.decode("utf8")
		return utfstr

	@staticmethod
	def decryption(content, key=constants.CRYPTE):
		"解密"
		de = list(b64encode(key))
		sc = content.replace("O0O0O", "=")
		_list = [sc[i:i + 2] for i in xrange(0, len(sc), 2)]
		xl = len(_list)
		for index, val in enumerate(de):
			if index < xl and len(_list[index]) > 1:
				if val == _list[index][1]:
					_list[index] = str(_list[index][0])
		try:
			return b64decode("".join(_list))
		except Exception as E:
			print E
			return u"解析出错,联系开发人员{str_list}".format(str_list="".join(_list))

	@staticmethod
	def cryption(content, key=constants.CRYPTE):
		"加密"
		de = list(b64encode(key))
		sc = list(b64encode(content))
		s_count = len(sc)
		for index, val in enumerate(de):
			if index < s_count:
				sc[index] += val
		return "".join(sc).replace("=", "O0O0O")

	@staticmethod
	def mkdir(path):
		# 去除首位空格
		path = path.strip()
		# 去除尾部 \ 符号
		path = path.rstrip("\\")
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False

	@staticmethod
	def set_style_excel(name="Times New Roman", height=None, bold=False, pattern=None):
		style = xlwt.XFStyle()  # 初始化样式\
		font = xlwt.Font()  # 为样式创建字体
		font.name = name if name else "Times New Roman"  # 'Times New Roman'
		font.bold = bold
		font.color_index = 4
		font.height = height if height else 220
		style.font = font

		borders = xlwt.Borders()
		borders.left = 1
		borders.right = 1
		borders.top = 1
		borders.bottom = 1
		borders.bottom_colour = 0x3A
		style.borders = borders

		if pattern:
			style.pattern = pattern
		return style

	@staticmethod
	def date_to_date(date):
		"""将yyyy-mm-dd 转化成 yyyymmdd"""
		if date is None:
			return date
		if "-" in date:
			return "".join(date.split("-"))
		else:
			return date

	@staticmethod
	def md5gen(pstr):
		import hashlib
		m = hashlib.md5()
		m.update(pstr)
		return m.hexdigest()

	@staticmethod
	def del_mobile_client_redis_banner():
		"""删除banner相关的redis"""
		all_keys = python_redis_store.keys()
		banner_keys = [key for key in all_keys if key.startswith("banner_list")]
		for bkey in banner_keys:
			python_redis_store.delete(bkey)
		return True

	@staticmethod
	def del_mobile_client_redis_news():
		"""删除news相关的redis"""
		all_keys = python_redis_store.keys()
		news_keys = [key for key in all_keys if key.startswith("news_list")]
		for nkey in news_keys:
			python_redis_store.delete(nkey)
		return True

	@staticmethod
	def del_mobile_client_redis_fast_news():
		"""删除快讯相关的redis"""
		all_keys = python_redis_store.keys()
		news_keys = [key for key in all_keys if key.startswith("fast_news_list")]
		for nkey in news_keys:
			python_redis_store.delete(nkey)
		return True


pubtool = PublicTools
