#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import FastNews
import json
import time
import logging
import os
from utils.timetools import TimeTools
from utils.util import pubtool
from werkzeug.utils import secure_filename
from configs.constants import NEWSURL
from application import quote_reids_store,qn
IMAGE_DIR = app.config.get("IMAGE_DIR")
IMAGE_SERVER = app.config.get("IMAGE_SERVER")

logger = logging.getLogger("views")
tt = TimeTools()
limit = 10


def get_total_page(total, limit):
	pageval = total % limit
	if pageval == 0:
		total_page = total / limit
	else:
		total_page = (total / limit) + 1
	return total_page


@app.route('/get_fast_news_list_total', methods=['GET', 'POST'])
@login_required
def get_fast_news_list_total():
	"""获取fast_news条数,并渲染页面"""
	info = {}
	if request.method == "POST":
		info = request.form
	elif request.method == "GET":
		info = request.values
	index = int(info.get("page", 1))
	total = FastNews.get_fast_news_list_total()
	total_page = get_total_page(total=total, limit=limit)
	page_serach = ""
	params = {}
	return render_template("operation_fast_news_list.html", params=params,
	                       pagination={"page": index, "total_page": total_page, "page_serach": page_serach,
	                                   "total": total})


@app.route('/fast_news_list_data', methods=['GET', 'POST'])
@login_required
def fast_news_list_data():
	"""获取fast_news列表数据"""
	info = request.values
	index = int(info.get("page", 1))
	fast_news_obj = FastNews.fast_news_list_data(index=index, limit=limit)
	fast_news_list = []
	for fast_news in fast_news_obj:
		_dict = {}
		_dict['id'] = fast_news.id
		_dict['title'] = fast_news.title
		_dict['subtitle'] = fast_news.subtitle
		_dict['desc'] = fast_news.desc
		_dict['author'] = fast_news.author
		# _dict['content'] = fast_news.content
		_dict['weight'] = fast_news.weight
		_dict['status'] = fast_news.status
		_dict['pub_time'] = tt.timestamp_to_timeformat(fast_news.pub_time) if fast_news.pub_time else '-'
		fast_news_list.append(_dict)
	return jsonify(fast_news_list=fast_news_list)


@app.route('/update_fast_news_status', methods=['GET', 'POST'])
@login_required
def update_fast_news_status():
	"""更新banner状态隐藏显示"""
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	_id = info.get('id')
	status = info.get('status')
	resp = FastNews.update_fast_news_status(id=_id, status=status)
	return jsonify(message='success', status=1)


@app.route('/del_fast_news', methods=['POST'])
@login_required
def del_fast_news():
	"""删除banner"""
	info = {}
	if request.method == "POST":
		info = request.values
	_id = info.get("id")
	if not _id:
		return jsonify(message="没有删除的fast_news", status=0)
	res = FastNews.del_fast_news(fast_news_id=_id)
	if res:
		return jsonify(message=res, status=0)
	return jsonify(message="success", status=1)



@app.route('/update_fast_news_weight', methods=['POST'])
@login_required
def update_fast_news_weight():
	"""修改fast_news权重"""
	info = {}
	if request.method == 'POST':
		info = request.values
	param = json.loads(info.get("param", []))
	if not param:
		return jsonify(message='没有需要修改权重的 NEWS 信息', status=0)
	result = FastNews.update_fast_news_weight(weight_list=param)
	if result:
		return jsonify(message=result, status=0)
	return jsonify(message='success', status=1)

def __get_fast_news_info(fast_news_id):
	"""获取快讯"""
	if fast_news_id == 0:
		return {}
	fast_news = FastNews.get_fast_news_details(fast_news_id=fast_news_id)
	if fast_news == None:
		return {}
	fast_news_dict = {}
	fast_news_dict["id"] = fast_news.id
	fast_news_dict["title"] = fast_news.title
	fast_news_dict["subtitle"] = fast_news.subtitle
	fast_news_dict["desc"] = fast_news.desc
	fast_news_dict["author"] = fast_news.author
	fast_news_dict["content"] = fast_news.content.replace("\n","")
	fast_news_dict['pub_time'] = fast_news.pub_time
	fast_news_dict["status"] = fast_news.status

	return fast_news_dict

@app.route('/get_fast_news_details', methods=['GET', 'POST'])
@login_required
def get_fast_news_details():
	"""banner详情"""
	fast_news_id = int(request.args.get("fast_news_id", 0))
	fast_news_detail = {}
	# 获取角色信息和权限id
	if fast_news_id > 0:
		fast_news_detail = __get_fast_news_info(fast_news_id)
	return render_template("operation_fast_news_details.html", fast_news_detail=fast_news_detail)



@app.route('/fast_news_details_edit', methods=['GET', 'POST'])
@login_required
def fast_news_details_edit():
	info = {}
	if request.method == "POST":
		info = request.values
	fast_news_id = int(info.get("fast_news_id")) if info.get("fast_news_id") else 0
	subtitle = info.get("subtitle","")
	title = info.get("title","")
	author = info.get("author","")
	content = info.get("content","")
	desc = info.get("desc","")
	cur_time = int(time.time())
	content = content.replace("\n",'').replace("'",'"')
	tdate= tt.today()
	if fast_news_id == 0:
		# 新增banner
		last_weight = FastNews.get_fast_news_weight()
		weight = last_weight + 1
		addstatus = FastNews.add_fast_news(title=title, subtitle=subtitle, author=author,tdate=tdate, cur_time=cur_time,
				              desc=desc, content=content,weight=weight)
		if addstatus:
			return jsonify(message=addstatus, status=0)
	elif fast_news_id > 0:
		editstatus = FastNews.edit_fast_news(title=title, subtitle=subtitle, author=author, cur_time=cur_time,
				              desc=desc, content=content,fast_news_id=fast_news_id)
		if editstatus:
			return jsonify(message=editstatus, status=0)
	else:
		pass
	return jsonify(message="success", status=1)


@app.route('/upload_fast_news_image', methods=['GET', 'POST'])
@login_required
def upload_fast_news_image():
	_path = tt.timepath_format()
	f = request.files["file"]
	fname = f.filename
	if not fname:
		return jsonify(message="请选择文件", status=1)
	filep = os.path.splitext(fname)
	if len(filep) < 2:
		return jsonify(message="文件格式不正确", status=1)
	filen, suffix = "fast_news", filep[1]
	save_path = IMAGE_DIR + _path
	pubtool.mkdir(path=save_path)
	curr_time = str(int(time.time()))
	filename = filen + '_' + curr_time + suffix
	filename = secure_filename(filename)  # 会把中文过滤掉,先替换,在检查
	local_file = save_path + "/" + filename
	f.save(local_file)
	imgsrc = qn.upload(qiniu_name=filename,local_file=local_file)
	# imgsrc = IMAGE_SERVER + "/" + _path + "/" + filename
	return jsonify(message="success", status=0, imgsrc=imgsrc)