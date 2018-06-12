#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import NewsRecommend
from app.news.models import News
import json
import logging
from utils.timetools import TimeTools

IMAGE_DIR = app.config.get("IMAGE_DIR")
IMAGE_SERVER = app.config.get("IMAGE_SERVER")

logger = logging.getLogger("views")
tt = TimeTools()
limit = 10


@app.route('/get_recommend_fixed', methods=['GET', 'POST'])
@login_required
def get_recommend_fixed():
	"""相关推荐"""
	info = request.values
	news_id = int(info.get("news_id")) if info.get("news_id") else 0
	recommends = NewsRecommend.get_news_recommend_fixed(news_id=news_id)
	all_news_list = News.news_list_data(status=1,index=1,limit=1000)
	return render_template("operation_recommend_details.html",news_id=news_id, news_list=recommends,all_news_list=all_news_list)

@app.route('/save_recommend_fixed', methods=['GET', 'POST'])
@login_required
def save_recommend_fixed():
	info = request.values
	_mult = info.get("mult", "[]")
	news_id = int(info.get("news_id", 0))
	if news_id == 0:
		return jsonify(msg='failed')
	mult = json.loads(_mult)
	res = NewsRecommend.update_news_recommend(mult=mult,news_id=news_id)
	if res == 0:
		return jsonify(status=1,message='success')
	return jsonify(status=0,message=res)
