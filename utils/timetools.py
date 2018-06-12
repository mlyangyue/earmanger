#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

import time
import datetime
from datetime import timedelta
class TimeTools(object):
	# 获取当前时间戳
	def timestamp(self):
		return int(time.time())

	def today(self):
		date_time = datetime.datetime.now()
		return int(date_time.strftime("%Y%m%d"))

	# 获取当前时间字符串 %Y-%m-%d %H:%M:%S
	def timeformat(self):
		import datetime
		#获得当前时间
		now = datetime.datetime.now()  # datetime.datetime(2016, 4, 27, 11, 23, 13, 811531)
		#转换为指定的格式:
		otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")  # str 2016-04-27 11:24:19
		return otherStyleTime

	def time_to_int(self):
		import datetime
		#获得当前时间
		now = datetime.datetime.now()  # datetime.datetime(2016, 4, 27, 11, 23, 13, 811531)
		#转换为指定的格式:
		otherStyleTime = now.strftime("%Y%m%d")  # str 20160427
		return int(otherStyleTime)


	def timepath_format(self,daystr=None):
		"""
		>>> datetime.datetime.now().strftime("%Y/%m/%d")
		>>>'2016/09/02'
		"""
		import datetime
		#获得当前时间
		now = datetime.datetime.now()  # datetime.datetime(2016, 4, 27, 11, 23, 13, 811531)
		#转换为指定的格式:
		otherStyleTime = now.strftime("%Y/%m/%d")  # str 2016/04/27
		return otherStyleTime

	# 根据时间字符串转换成时间戳
	def timetarn(self,timestr=None):
		if not timestr:
			return time.time()
		if isinstance(timestr,basestring):
			#将其转换为时间数组
			timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # time.struct_time(tm_year=2013, tm_mon=10, tm_mday=10, tm_hour=23, tm_min=40, tm_sec=0, tm_wday=3, tm_yday=283, tm_isdst=-1)
			#转换为时间戳:
			return time.mktime(timeArray)
		return None

	# 根据datetime转换成str
	def datetime_to_str(self,source_time=None):
		if not source_time:
			return self.timeformat()
		return source_time.strftime("%Y-%m-%d %H:%M:%S")

	#时间戳格式化为时间字符串
	def timestamp_to_timeformat(self,t_stamp=None):
		"""
		时间戳转时间字符串
		"""
		if not t_stamp:
			t_stamp = self.timestamp()
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t_stamp))
	#时间戳 格式化为 日期时间(2017-11-21)
	def timestamp_to_date(self, date_stamp=None):
		"""
		#时间戳 格式化为 日期时间(2017-11-21)
		:return:
		"""
		return time.strftime('%Y-%m-%d', time.localtime(date_stamp))

	def datetimeplus(self,val=0,ptype="days",start_time=None):
		if not start_time:
			today = datetime.datetime.now()
		else:
			today = datetime.datetime.strptime(start_time,'%Y-%m-%d')
		if ptype=="days":
			return  today + datetime.timedelta(days=val)

	def datetime_to_timestamp(self,d_time):
		"""
		date转时间戳
		"""
		if not d_time:
			return self.timestamp()
		return int(time.mktime(d_time.timetuple()))

		
	def date_to_date(self, date):
		"""将 yyyy-mm-dd  转化成  yyyymmdd"""
		if date is None:
			return date
		if "-" in date:
			return "".join(date.split("-"))
		else:
			return date

	def intDate_to_strDate(self, date):
		"""将 yyyymmdd  转化成 yyyy-mm-dd"""
		if date is None:
			return date
		date = str(date)
		result = date[0:4] +"-"+ date[4:6] +"-"+ date[6:8]
		return result
	def date_to_n_date_later(self,days):
		'''  获取 N 天之后的日期   '''
		n_date = datetime.datetime.now() + timedelta(days=days)
		n_date = n_date.strftime('%Y%m%d')
		return n_date
	
	# 这天的开始时间戳
	def dateday_to_timestamp(self, date_str=None):
		""" 这天的开始时间戳"""
		if date_str is None:
			day = str(self.today())
		else:
			day = date_str
		day_tuple = time.strptime(day, "%Y%m%d")  # time.struct_time(tm_year=2013, tm_mon=10, tm_mday=10, tm_hour=23, tm_min=40, tm_sec=0, tm_wday=3, tm_yday=283, tm_isdst=-1)
		day_timestamp = time.mktime(day_tuple)
		return day_timestamp

	def compare_time_span(self, start_hour, start_min, end_hour, end_min, current):
		start = datetime.time(start_hour, start_min)
		end = datetime.time(end_hour, end_min)
		return (start <= current <= end)

