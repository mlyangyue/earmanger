#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import BackUser
import json
import logging
from utils.timetools import TimeTools
from utils.util import PublicTools
from application import quote_reids_store
logger = logging.getLogger("views")
tt = TimeTools()
limit = 10


@app.route('/user_role', methods=['GET', 'POST'])
@login_required
def user_role():
	user_id = g.user.id
	showall = g.user.showall
	index = int(request.args.get("page", 1))
	user_role_list, total = BackUser.query_role_list(index=index, limit=limit,uid=user_id, showall=showall)
	pageval = total % limit
	if pageval == 0:
		total_page = total / limit
	else:
		total_page = total / limit + 1
	return render_template("user_role.html", user_role_list=user_role_list, params={},
	                       pagination={"page": index, "total_page": total_page,"total":total})


@app.route('/user_role_details', methods=['GET', 'POST'])
@login_required
def user_role_details():
	"""角色详情"""
	role_id = int(request.args.get("role_id", 0))
	user_role = {}
	ele_list = []
	# 获取角色信息和权限id
	if role_id > 0:
		user_role, ele_list = __get_role_info(role_id)
	element_info = BackUser.query_element_info()
	authority = __all_element_info(element_info)
	return render_template("user_role_details.html", user_role=user_role, ele_list=ele_list, authority=authority)


def __get_role_info(role_id):
	"""获取角色信息和权限id"""
	if role_id == 0:
		return {}, []
	roleobj = BackUser.query_role_info(role_id)
	role_element_list = []
	if roleobj:
		requery = BackUser.query_role_element(role_id)
		for item in requery:
			role_element_list.append(int(item.element_id))
	return roleobj, role_element_list


def __all_element_info(element_info):
	"""所有元素权限"""
	_dict = {}
	try:
		for entry in element_info:
			id = int(entry.id)
			name = entry.name
			etype = int(entry.etype)
			father_id = int(entry.father_id)
			if etype == 1:
				if id not in _dict.keys():
					_dict[id] = {}
					_dict[id]["id"] = id
					_dict[id]["name"] = name
					_dict[id]["second"] = []
				pass
			if etype == 2:
				_dict[father_id]["second"].append({"id": id, "name": name, "third": []})
				# _dict[father_id]["second"].append({"id": id, "name": name, "ele": []})
			if etype == 3:
				for key, val in _dict.iteritems():
					# key是一级菜单id
					for item in val['second']:
						if father_id != item["id"]:
							continue
						item["third"].append({"id": id, "name": name, "ele":[]})
					pass
				pass
			if etype == 4:
				for key, val in _dict.iteritems():
					for item in val['second']:
						for eles in item["third"]:
							if father_id != eles["id"]:
								continue
							eles["ele"].append({"id": id, "name": name})
	except Exception as E:
		print E
		logger.info(E)
		return _dict
	return _dict


@app.route('/user_role_edit', methods=['GET', 'POST'])
@login_required
def user_role_edit():
	uid = g.user.id
	info = request.values
	role_id = int(info.get("group_id", 0))
	role_name = info.get("group_name", "")
	role_remark = info.get("group_remark", "")
	_auths = info.get("auths", "[]")
	auths = json.loads(_auths)
	if role_id == 0:
		# 检查角色名称是否存在
		res = BackUser.query_user_role(role_name)
		if res:
			return jsonify(message=res, status=0)
		# 新增
		addstatus = BackUser.add_user_role(group_name=role_name, group_remark=role_remark, group_auth=auths, created_id=uid)
		if addstatus:
			return jsonify(message=addstatus, status=0)
	elif role_id > 0:

		editstatus = BackUser.edit_user_role(role_name=role_name, role_id=role_id, role_remark=role_remark,
		                                     role_auth=auths)
		if editstatus:
			return jsonify(message=editstatus, status=0)
	else:
		pass
	return jsonify(message="success", status=1)


@app.route('/user_backend_user', methods=['GET', 'POST'])
@login_required
def user_backend_user():
	"""后台用户管理"""
	uid = g.user.id
	showall = g.user.showall
	index = int(request.args.get("page", 1))
	user_list, total = BackUser.query_user_list(index=index, limit=limit,uid=uid,showall=showall)
	pageval = total % limit
	if pageval == 0:
		total_page = total / limit
	else:
		total_page = total / limit + 1
	return render_template("user_backend_user.html", user_list=user_list, params={},
	                       pagination={"page": index, "total_page": total_page,"total":total})


@app.route('/user_backend_details', methods=['GET', 'POST'])
@login_required
def user_backend_details():
	"""角色详情"""
	uid = g.user.id
	showall = g.user.showall
	user_id = int(request.args.get("user_id", 0))
	# 获取所有角色
	role_list, total = BackUser.query_role_list(islimit=0,uid=uid,showall=showall)
	user_info = {}
	user_role = []
	# 获取角色信息和权限id
	if user_id > 0:
		user_info = BackUser.query_backend_user_info(user_id)
		user_role = __get_user_role(user_id)
	return render_template("user_backend_details.html", user_info=user_info, role_list=role_list, user_role=user_role)


def __get_user_role(user_id):
	"""获取用户角色"""
	userrole = BackUser.query_backend_user_role(user_id=user_id)
	user_role = []
	for entry in userrole:
		user_role.append(int(entry.role_id))
	return user_role


@app.route('/user_backend_edit', methods=['GET', 'POST'])
@login_required
def user_backend_edit():
	uid = g.user.id
	info = request.values
	user_id = int(info.get("user_id", 0))
	user_name = info.get("user_name", "")
	real_name = info.get("real_name", "")
	pass_word = info.get("pass_word", "")
	if pass_word:
		pass_word = PublicTools.md5gen(pass_word)
	_mult = info.get("mult", "[]")
	mult = json.loads(_mult)
	if user_id == 0:
		# 检查用户名是否存在
		res = BackUser.query_user_backend(user_name)
		if res:
			return jsonify(message=res, status=0)
		# 新增
		addstatus = BackUser.add_user_backend(user_name=user_name, password=pass_word, real_name=real_name,
		                                      role_mult=mult,created_id=uid)
		if addstatus:
			return jsonify(message=addstatus, status=0)
	elif user_id > 0:

		editstatus = BackUser.edit_user_backend(user_id=user_id, user_name=user_name, password=pass_word,
		                                        real_name=real_name, role_mult=mult)
		if editstatus:
			return jsonify(message=editstatus, status=0)
	else:
		pass
	return jsonify(message="success", status=1)


@app.route('/recharge_switch_settings', methods=['GET', 'POST'])
@login_required
def recharge_switch_settings():
	switch_dict = BackUser.get_switch_info()
	switch_info_dict = BackUser.get_switch_info_dict()
	return render_template('system_params.html', switch_dict=switch_dict, switch_info_dict=switch_info_dict)

@app.route('/modify_pay_switch', methods=['GET', 'POST'])
@login_required
def modify_pay_switch():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	pay_switch = info.get('pay_switch', 1)
	switch_info = info.get('switch_info', '')
	pay_switch_info = BackUser.modify_pay_switch(pay_switch=pay_switch, switch_info=switch_info)
	if pay_switch_info:
		return jsonify(status=1,msg='success')
	return jsonify(status=0,msg='failed')


@app.route('/modify_scan_wechat', methods=['GET', 'POST'])
@login_required
def modify_scan_wechat():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	scan_wechat = info.get('scan_wechat', 1)
	switch_info = info.get('switch_info', '')
	pay_switch_info = BackUser.modify_scan_wechat(scan_wechat=scan_wechat, switch_info=switch_info)
	if pay_switch_info:
		return jsonify(status=1,msg='success')
	return jsonify(status=0,msg='failed')

@app.route('/modify_web_scan_wechat', methods=['GET', 'POST'])
@login_required
def modify_web_scan_wechat():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	web_scan_wechat = info.get('web_scan_wechat', 1)
	switch_info = info.get('switch_info', '')
	pay_switch_info = BackUser.modify_web_scan_wechat(web_scan_wechat=web_scan_wechat, switch_info=switch_info)
	if pay_switch_info:
		return jsonify(status=1,msg='success')
	return jsonify(status=0,msg='failed')

@app.route('/modify_scan_alipay', methods=['GET', 'POST'])
@login_required
def modify_scan_alipay():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	scan_alipay = info.get('scan_alipay', 1)
	switch_info = info.get('switch_info', '')
	pay_switch_info = BackUser.modify_scan_alipay(scan_alipay=scan_alipay, switch_info=switch_info)
	if pay_switch_info:
		return jsonify(status=1,msg='success')
	return jsonify(status=0,msg='failed')


@app.route('/modify_web_scan_alipay', methods=['GET', 'POST'])
@login_required
def modify_web_scan_alipay():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	web_scan_alipay = info.get('web_scan_alipay', 1)
	switch_info = info.get('switch_info', '')
	pay_switch_info = BackUser.modify_web_scan_alipay(web_scan_alipay=web_scan_alipay, switch_info=switch_info)
	if pay_switch_info:
		return jsonify(status=1,msg='success')
	return jsonify(status=0,msg='failed')


@app.route('/modify_web_bank', methods=['GET', 'POST'])
@login_required
def modify_web_bank():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	web_bank = info.get('web_bank', 1)
	switch_info = info.get('switch_info', '')
	web_bank = BackUser.modify_web_bank(web_bank=web_bank, switch_info=switch_info)
	if web_bank:
		return jsonify(status=1, msg='success')
	return jsonify(status=0, msg='failed')

@app.route('/get_phone_parameter_list',methods=['GET','POST'])
@login_required
def get_phone_parameter_list():
	info = {}
	total = 0
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	index = int(info.get('page',1))
	parameter_list,total = BackUser.get_phone_parameter(index=index,limit=limit)
	pageval = total % limit
	if pageval == 0:
		total_page = total / limit
	else:
		total_page = total / limit + 1
	return render_template('phone_parameter_list.html',parameter_list=parameter_list,
						   pagination={"page": index, "total_page": total_page, "total": total})

@app.route('/edit_phone_parameter',methods=['GET','POST'])
@login_required
def edit_phone_parameter():

	parameter_id = int(request.args.get('parameter_id',0))
	parameter_info = {}
	if parameter_id > 0:
		parameter_info = BackUser.get_phone_parameter_info(parameter_id=parameter_id)
	return render_template('phone_parameter_info.html',parameter_info=parameter_info)

@app.route('/get_invite_switch', methods=["GET", "POST"])
@login_required
def get_invite_switch():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	forbid_user_wenan = quote_reids_store.get('user_limit_login_msg').decode('utf-8') if quote_reids_store.get('user_limit_login_msg') else ''
	invite_switch,wen_an = BackUser.get_invite_switch()
	switch = int(invite_switch.value)
	wen_an_info = wen_an.invitecode
	# app 滚动信息
	roll_info = quote_reids_store.get('hq_roll_msg')
	_info_dict = {}
	if roll_info:
		roll_info = json.loads(roll_info)
		_info_dict['start'] = tt.timestamp_to_date(roll_info['start'])
		_info_dict['end'] = tt.timestamp_to_date(roll_info['end'])
		_info_dict['insert'] = roll_info['insert']
		_info_dict['status'] = roll_info['status']
		_info_dict['info'] = roll_info['info']
	else:
		_info_dict = info
	params = {}
	params["invite_switch"] = switch
	params['wen_an'] = wen_an_info
	return render_template('client_params.html',params=params,forbid_user_wenan=forbid_user_wenan, roll_info=_info_dict)


@app.route('/save_roll_info', methods=['GET', 'POST'])
@login_required
def save_roll_info():
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	start_time = info.get('start', '')
	end_time = info.get('end', '')
	status = int(info.get('roll_check', 0))
	msg = info.get('info', '')

	start_date = start_time
	end_date = end_time
	if start_time and end_time:
		start_date = start_time if start_time < end_time else end_time
		end_date = start_time if start_time > end_time else end_time
	elif not start_time:
		end_date = end_time
	elif not end_time:
		start_date = start_date
	start_stamp = 0
	end_stamp = 0
	if start_date:
		start_date = start_date + " 0:00:00"
		start_stamp = tt.timetarn(start_date)
	if end_date:
		end_date = end_date + " 23:59:59"
		end_stamp = tt.timetarn(end_date)
	current_time = tt.timestamp()
	quote_reids_store.set('hq_roll_msg',json.dumps({'start':start_stamp,'end':end_stamp,'status':status,'info':msg,'insert':current_time}))
	return jsonify(msg='success', status=1)

@app.route('/change_client_invite_switch', methods=["GET", "POST"])
@login_required
def change_client_invite_switch():
	info = {}
	if request.method == 'POST':
		info = request.form
	invite_switch = int(info.get('invite_switch', 2))
	invite_wen_an = info.get('invite_wen_an', '')
	invite_info = BackUser.change_invite_switch(invite_code=invite_switch)
	invite_wenan_info = BackUser.modify_wenan_info(invite_wen_an=invite_wen_an)
	return jsonify(message='success', status=1)



@app.route('/modify_parameter_info',methods=['GET','POST'])
@login_required
def modify_parameter_info():
	info = {}
	if request.method == 'POST':
		info = request.form
	parameter_id = info.get('parameter_id',0)
	version_num = info.get('version_num','')
	check_box = info.get('check_box',0)
	webpay = info.get('webpay','')
	weixinpay = info.get('weixinpay','')
	phonepay = info.get('phonepay','')
	phone_web_pay = info.get('phone_web_pay','')
	scanpay = info.get('scan_pay','')
	disablepay = info.get('disablepay', '')
	disablepay_switch = info.get('disablepay_switch', 1)
	loan_wenan = info.get('loan_wenan', '')
	disable_loan_wenan = info.get('disable_loan_wenan', '')

	current_time = tt.timestamp()
	parameter_info = BackUser.modify_phone_info(version_num=version_num,check_box=check_box,parameter_id=parameter_id,scanpay=scanpay,
												current_time=current_time,webpay=webpay,weixinpay=weixinpay,phonepay=phonepay,
												phone_web_pay=phone_web_pay,disablepay=disablepay,disablepay_switch=disablepay_switch,
												loan_wenan=loan_wenan,disable_loan_wenan=disable_loan_wenan)
	return jsonify(message="success",status=1)

@app.route('/modify_forbid_user_wenan', methods=['GET', 'POST'])
@login_required
def modify_forbid_user_wenan():
	info = {}
	if request.method == 'POST':
		info = request.form
	elif request.method == 'GET':
		info = request.values
	forbid_wenan = info.get('forbid_wenan', '')
	quote_reids_store.set('user_limit_login_msg', forbid_wenan)
	return jsonify(msg='success', status=1)