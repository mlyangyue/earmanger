#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import News
import json
import time
import logging
import os
from utils.timetools import TimeTools
from utils.util import pubtool
from werkzeug.utils import secure_filename
from application import qn
IMAGE_DIR = app.config.get("IMAGE_DIR")

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


@app.route('/get_news_list_total', methods=['GET', 'POST'])
@login_required
def get_news_list_total():
	"""获取news条数,并渲染页面"""
	info = {}
	if request.method == "POST":
		info = request.form
	elif request.method == "GET":
		info = request.values
	index = int(info.get("page", 1))
	total = News.get_news_list_total()
	total_page = get_total_page(total=total, limit=limit)
	page_serach = ""
	params = {}
	return render_template("operation_news_list.html", params=params,
	                       pagination={"page": index, "total_page": total_page, "page_serach": page_serach,
	                                   "total": total})


@app.route('/news_list_data', methods=['GET', 'POST'])
@login_required
def news_list_data():
	"""获取news列表数据"""
	info = request.values
	index = int(info.get("page", 1))
	news_obj = News.news_list_data(index=index, limit=limit)
	news_list = []
	for news in news_obj:
		_dict = {}
		_dict['id'] = news.id
		_dict['title'] = news.title
		_dict['subtitle'] = news.subtitle
		_dict['desc'] = news.desc
		_dict['author'] = news.author
		# _dict['content'] = news.content
		_dict['read_num'] = news.read_num
		_dict['weight'] = news.weight
		_dict['status'] = news.status
		_dict['real_read'] = news.real_read
		_dict['small_pic'] = news.small_pic
		_dict['details_url'] = news.details_url
		_dict['pub_time'] = tt.timestamp_to_timeformat(news.pub_time) if news.pub_time else '-'
		news_list.append(_dict)
	return jsonify(news_list=news_list)


@app.route('/update_news_status', methods=['GET', 'POST'])
@login_required
def update_news_status():
	"""更新banner状态隐藏显示"""
	info = {}
	if request.method == 'GET':
		info = request.values
	elif request.method == 'POST':
		info = request.form
	_id = info.get('id')
	status = info.get('status')
	resp = News.update_news_status(id=_id, status=status)
	return jsonify(message='success', status=1)


@app.route('/del_news', methods=['POST'])
@login_required
def del_news():
	"""删除banner"""
	info = {}
	if request.method == "POST":
		info = request.values
	_id = info.get("id")
	if not _id:
		return jsonify(message="没有删除的banner", status=0)
	res = News.del_news(news_id=_id)
	if res:
		return jsonify(message=res, status=0)
	return jsonify(message="success", status=1)



@app.route('/update_news_weight', methods=['POST'])
@login_required
def update_news_weight():
	"""修改news权重"""
	info = {}
	if request.method == 'POST':
		info = request.values
	param = json.loads(info.get("param", []))
	if not param:
		return jsonify(message='没有需要修改权重的 NEWS 信息', status=0)
	result = News.update_news_weight(weight_list=param)
	if result:
		return jsonify(message=result, status=0)
	return jsonify(message='success', status=1)

def __get_news_info(news_id):
	"""获取news"""
	if news_id == 0:
		return {}
	news = News.get_news_details(news_id=news_id)
	if news == None:
		return {}
	news_dict = {}
	news_dict["id"] = news.id
	news_dict["title"] = news.title
	news_dict["subtitle"] = news.subtitle
	news_dict["desc"] = news.desc
	news_dict["author"] = news.author
	news_dict["small_pic"] = news.small_pic
	news_dict["read_num"] = news.read_num
	news_dict["content"] = news.content.replace("\n","")
	news_dict['details_url'] = news.details_url
	news_dict['pub_time'] = news.pub_time
	news_dict["status"] = news.status

	return news_dict

@app.route('/get_news_details', methods=['GET', 'POST'])
@login_required
def get_news_details():
	"""news详情"""
	news_id = int(request.args.get("news_id", 0))
	news_detail = {}
	# 获取角色信息和权限id
	if news_id > 0:
		news_detail = __get_news_info(news_id)
	return render_template("operation_news_details.html", news_detail=news_detail)



@app.route('/news_details_edit', methods=['GET', 'POST'])
@login_required
def news_details_edit():
	info = {}
	if request.method == "POST":
		info = request.values
	news_id = int(info.get("news_id")) if info.get("news_id") else 0
	small_pic = info.get("small_pic","")
	subtitle = info.get("subtitle","")
	title = info.get("title","")
	author = info.get("author","")
	content = info.get("content","")
	desc = info.get("desc","")
	read_num = int(info.get("read_num")) if info.get("read_num") else 0
	cur_time = int(time.time())
	content = content.replace("\n",'').replace("'",'"')
	tdate= tt.today()
	if news_id == 0:
		# 新增news
		last_weight = News.get_news_weight()
		weight = last_weight + 1
		addstatus = News.add_news(title=title, subtitle=subtitle, author=author, read_num=read_num,tdate=tdate, cur_time=cur_time,
				              desc=desc, content=content,weight=weight,small_pic=small_pic)
		if addstatus:
			return jsonify(message=addstatus, status=0)
	elif news_id > 0:
		editstatus = News.edit_news(title=title, subtitle=subtitle, author=author, read_num=read_num, cur_time=cur_time,
				              desc=desc, content=content,news_id=news_id,small_pic=small_pic)
		if editstatus:
			return jsonify(message=editstatus, status=0)
	else:
		pass
	return jsonify(message="success", status=1)


@app.route('/upload_news_image', methods=['GET', 'POST'])
@login_required
def upload_news_image():
	_path = tt.timepath_format()
	f = request.files["file"]
	fname = f.filename
	if not fname:
		return jsonify(message="请选择文件", status=1)
	filep = os.path.splitext(fname)
	if len(filep) < 2:
		return jsonify(message="文件格式不正确", status=1)
	filen, suffix = "news", filep[1]
	save_path = IMAGE_DIR + _path
	pubtool.mkdir(path=save_path)
	curr_time = str(int(time.time()))
	filename = filen + '_' + curr_time + suffix
	filename = secure_filename(filename)  # 会把中文过滤掉,先替换,在检查
	local_file = save_path + "/" + filename
	f.save(local_file)
	imgsrc = qn.upload(qiniu_name=filename,local_file=local_file)
	return jsonify(message="success", status=0, imgsrc=imgsrc)