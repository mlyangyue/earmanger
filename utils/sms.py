#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Han Yong bo'

import urllib2
import urllib
import  xml.dom.minidom
import logging
import hashlib

logger = logging.getLogger("views")

class Sms_NEW:
	''' 短信通道配置参数 '''
	account  = 'haotouguyx'  # 账户名
	password = 'haotouguyx'  # 密码
	userid   = '214'  # 企业id
	# userid   = '317'  # 企业id
	url 	 = 'http://123.57.176.126:8888/sms.aspx?action=send'  # utf-8请求地址
	# url 	 = 'http://115.29.196.232:8888/sms.aspx?action=send'  # utf-8请求地址


	@staticmethod
	def mass_send(mobile,content,stime=''):
		'''请求数据'''
		print mobile
		data = {}
		data['userid']   = Sms_NEW.userid
		data['account']  = Sms_NEW.account
		data['password'] = Sms_NEW.password
		data['mobile'] 	= mobile
		data['content'] = '【好投顾】'+content+',退订回N。'
		data['sendTime'] = stime
		data['checkcontent'] = '1'
		result = Sms_NEW.SendSms(data,Sms_NEW.url)
		return result

	@staticmethod
	def SendSms(data,url):
		'''发送短信'''
		try:
			post_data = urllib.urlencode(data)
			req = urllib2.Request(url=url, data=post_data)
			res_data = urllib2.urlopen(req)
			res = res_data.read()
			dom = xml.dom.minidom.parseString(res)
			result = dom.getElementsByTagName("returnstatus")
			result = result[0].childNodes[0].nodeValue
			if result != 'Success':
				logger.info("短信发送结果,err = {error}".format(error=result))
				return False
			else:
				return True
		except Exception as error:
			print error
			logger.info("发送短信,err = {error}".format(error=error))
			return False

class Sms:
	''' 短信通道配置参数 '''
	sn  = 'SDK-BBX-010-25690'  # 账户名
	pwd = '1Ae81-A109-'  # 密码
	url = "http://sdk.entinfo.cn:8061/webservice.asmx/mdsmssend"
	@staticmethod
	def mass_send(mobile,content,stime=''):
		'''请求数据'''
		data = {}
		send_url = Sms.url
		data["sn"]  = Sms.sn
		data["pwd"] = Sms.md5_get_upper(Sms.sn+Sms.pwd)
		data["mobile"] 	= mobile
		data["content"] = '【好投顾APP】'+content+'退订回N'
		data["ext"] = ''
		data["stime"] = stime
		data["rrid"] = ''
		data["msgfmt"] = ''
		result = Sms.SendSms(data,send_url)

		return result

	@staticmethod
	def md5_get_upper(snpwd):
		"""MD5 加密"""
		md5obj = hashlib.md5()
		md5obj.update(snpwd)
		md5str = md5obj.hexdigest().upper()
		return md5str

	@staticmethod
	def SendSms(data,url):
		'''发送短信'''
		try:
			post_data = urllib.urlencode(data)
			req = urllib2.Request(url=url, data=post_data)
			res_data = urllib2.urlopen(req)
			res = res_data.read()
			logger.info("短信发送结果,err = {error},数据={data}".format(error=res,data=data))
			dom = xml.dom.minidom.parseString(res)
			result = dom.getElementsByTagName("string")
			result = result[0].childNodes[0].nodeValue
			if result.isdigit() and int(result)>0 and len(result)==18:
				return True
			else:
				logger.error("短信发送结果,err = {error}".format(error=result))
				return False

		except Exception as error:
			print error
			logger.error("发送短信,err = {error}".format(error=error))
			return False

if __name__=="__main__":
	# mobile="15710051969,13146993034,18910693021"
	# print Sms.mass_send(mobile=mobile,content="测试2定时发送2016-12-16 17:40:00",stime="2016-12-16 17:40:00")
	mobile='13146993034,18518925067'
	print Sms_NEW.mass_send(mobile=mobile,content="测试立即发送多个手机号短信是否正常",stime="2017-03-20 16:30:00")