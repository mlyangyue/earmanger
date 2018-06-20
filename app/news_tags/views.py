#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app
from flask.ext.login import login_required
from flask import request, jsonify, g, render_template
from models import NewsTags
import logging
import json
from utils.timetools import TimeTools

logger = logging.getLogger("views")
tt = TimeTools()


@app.route('/get_news_tags', methods=['GET', 'POST'])
@login_required
def get_news_tags():
	"""获取"""
	info = request.values
	news_id = int(info.get("news_id")) if info.get("news_id") else 0
	news_tags = NewsTags.get_news_tags(news_id=news_id)
	return jsonify(news_tags=news_tags)

@app.route('/get_common_news_tags', methods=['GET', 'POST'])
@login_required
def get_common_news_tags():
	"""获取常用新闻标签"""
	common_tags = NewsTags.get_common_news_tags(ptype=0)
	return jsonify(common_tags=common_tags)



@app.route('/save_news_tags', methods=['GET', 'POST'])
@login_required
def save_news_tags():
	info = request.values
	news_id = int(info.get("news_id")) if info.get("news_id") else 0
	tags_arr = json.loads(info.get("tags_arr",'')) if info.get("tags_arr") else []
	if not tags_arr:
		return jsonify(msg='无标签',status=1)
	NewsTags.save_news_tags(news_id=news_id,tags_arr=tags_arr)
	return jsonify(msg='成功',status=1)
