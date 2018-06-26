#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import Banner
from app.news.models import News
import json
import os
import time
import logging
from utils.timetools import TimeTools
from utils.util import pubtool
from werkzeug.utils import secure_filename
from application import qn

logger = logging.getLogger("views")
tt = TimeTools()
limit = 10
IMAGE_DIR = app.config.get("IMAGE_DIR")


def get_total_page(total, limit):
	pageval = total % limit
	if pageval == 0:
		total_page = total / limit
	else:
		total_page = (total / limit) + 1
	return total_page


@app.route('/get_banner_list_total', methods=['GET', 'POST'])
@login_required
def get_banner_list_total():
	"""获取新闻条数,并渲染页面"""
	info = {}
	if request.method == "POST":
		info = request.form
	elif request.method == "GET":
		info = request.values
	index = int(info.get("page", 1))
	banner_type = info.get("banner_type", "")
	total = Banner.get_banner_list_total(banner_type=banner_type)
	total_page = get_total_page(total=total, limit=limit)
	page_serach = u"&banner_type={banner_type}".format(banner_type=banner_type)
	params = {}
	params["banner_type"] = banner_type
	return render_template("operation_banner_list.html", params=params,
	                       pagination={"page": index, "total_page": total_page, "page_serach": page_serach,
	                                   "total": total})


@app.route('/banner_list_data', methods=['GET', 'POST'])
@login_required
def banner_list_data():
	"""获取banner列表数据"""
	info = request.values
	index = int(info.get("page", 1))
	banner_type = info.get("banner_type", "")
	banner_obj = Banner.banner_list_data(banner_type=banner_type, index=index, limit=limit)
	banner_list = []
	for banner in banner_obj:
		_dict = {}
		_dict['id'] = banner.id
		_dict['pic'] = banner.pic
		_dict['url'] = banner.url
		_dict['btype'] = banner.btype
		_dict['weight'] = banner.weight
		_dict['jtype'] = banner.jtype
		_dict['status'] = banner.status
		_dict['created_time'] = banner.created_time
		_dict['last_time'] = banner.last_time
		banner_list.append(_dict)
	return jsonify(banner_list=banner_list)


@app.route('/update_banner_status', methods=['GET', 'POST'])
@login_required
def update_banner_status():
	"""更新banner状态隐藏显示"""
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	_id = info.get('id')
	status = info.get('status')
	resp = Banner.update_banner_status(id=_id, status=status)
	return jsonify(message='success', status=1)


@app.route('/del_banner', methods=['POST'])
@login_required
def del_banner():
	"""删除banner"""
	info = {}
	if request.method == "POST":
		info = request.values
	_id = info.get("id")
	if not _id:
		return jsonify(message="没有删除的banner", status=0)
	res = Banner.del_banner(banner_id=_id)
	if res:
		return jsonify(message=res, status=0)
	return jsonify(message="success", status=1)


@app.route('/update_banner_weight', methods=['POST'])
@login_required
def update_banner_weight():
	"""修改banner权重"""
	info = {}
	if request.method == "POST":
		info = request.values
	param = json.loads(info.get("param", "[]"))
	if not param:
		return jsonify(message="没有需要修改权重的banner", status=0)
	res = Banner.update_banner_weight(weight_list=param)
	if res:
		return jsonify(message=res, status=0)
	return jsonify(message="success", status=1)


def __get_banner_info(banner_id):
	"""获取banner"""
	if banner_id == 0:
		return {}
	banner = Banner.get_banner_details(banner_id=banner_id)
	if banner == None:
		return {}
	banner_dict = {}
	banner_dict["id"] = banner.id
	banner_dict["pic"] = banner.pic
	banner_dict["btype"] = banner.btype
	banner_dict["jtype"] = banner.jtype
	banner_dict['url'] = banner.url
	banner_dict["status"] = banner.status
	banner_dict["jid"] = banner.jid
	print banner.jid
	return banner_dict


@app.route('/get_banner_details', methods=['GET', 'POST'])
@login_required
def get_banner_details():
	"""banner详情"""
	banner_id = int(request.args.get("banner_id", 0))
	banner_detail = {}
	"""获取新闻详情,跳转链接"""
	news_list = News.news_list_data(status=1, index=1, limit=1000)
	banner_detail['news_list'] = news_list
	# 获取角色信息和权限id
	if banner_id > 0:
		banner_detail = __get_banner_info(banner_id)
	banner_detail['news_list'] = news_list
	return render_template("opteration_banner_details.html", banner_detail=banner_detail)


@app.route('/banner_details_edit', methods=['GET', 'POST'])
@login_required
def banner_details_edit():
	info = {}
	if request.method == "POST":
		info = request.values
	banner_id = int(info.get("banner_id")) if info.get("banner_id") else 0
	banner_url = info.get("banner_url")
	btype = int(info.get("btype", 0))
	jtype = int(info.get("jtype", 0))
	news_id = int(info.get("news_id", 0)) if info.get("news_id", 0) else ''
	status = int(info.get('status', 0))
	cur_time = int(time.time())
	jump_url = ''
	if news_id:
		news_detail = News.get_news_details(news_id=news_id)
		jump_url = news_detail.details_url
	if banner_id == 0:
		# 新增banner
		last_weight = Banner.get_banner_weight(btype=btype)
		weight = last_weight + 1
		addstatus = Banner.add_banner(banner_url=banner_url, btype=btype, jtype=jtype, jump_url=jump_url,
		                              weight=weight, cur_time=cur_time, jid=news_id, status=status)
		if addstatus:
			return jsonify(message=addstatus, status=0)
	elif banner_id > 0:
		editstatus = Banner.edit_banner(banner_url=banner_url, btype=btype, jtype=0, jump_url=jump_url,
		                                banner_id=banner_id, cur_time=cur_time, jid=news_id,
		                                status=status)
		if editstatus:
			return jsonify(message=editstatus, status=0)
	else:
		pass
	return jsonify(message="success", status=1)


@app.route('/upload_banner_image', methods=['GET', 'POST'])
@login_required
def upload_banner_image():
	_path = tt.timepath_format()
	f = request.files["file"]
	fname = f.filename
	if not fname:
		return jsonify(message="请选择文件", status=1)
	filep = os.path.splitext(fname)
	if len(filep) < 2:
		return jsonify(message="文件格式不正确", status=1)
	filen, suffix = "banner", filep[1]
	save_path = IMAGE_DIR + _path
	pubtool.mkdir(path=save_path)
	curr_time = str(int(time.time()))
	filename = filen + '_' + curr_time + suffix
	filename = secure_filename(filename)  # 会把中文过滤掉,先替换,在检查
	local_file = save_path + "/" + filename
	f.save(local_file)
	imgsrc = qn.upload(qiniu_name=filename, local_file=local_file)
	return jsonify(message="success", status=0, imgsrc=imgsrc)
