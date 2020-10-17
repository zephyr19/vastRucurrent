# -*- coding: utf-8 -*-
import sys
import os
import django
from django.db import connection
import math
import copy

import numpy as np

# 找到项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RadiationVis.settings')
django.setup()

# [left, bottom, right, top]
extent = [-120.0, 0.0, -119.711751, 0.238585]
span = 0.01
m = math.ceil(abs(extent[1]-extent[3])/span)
n = math.ceil(abs(extent[0]-extent[2])/span)

left = extent[0]
right = extent[0] + n * span
top = extent[3]
bottom = extent[3] - m * span

def getRad(d):
	return d * math.pi / 180.0

def distanceByLnglat(lat1, lng1, lat2, lng2):
	radLat1 = getRad(lat1)
	radLat2 = getRad(lat2)
	a = radLat1 - radLat2
	b = getRad(lng1) - getRad(lng2)
	s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
	s = s * 6378137.0
	s = round(s * 10000) / 10000
	return s

def idw(griddata):
	copy_data = copy.deepcopy(griddata)
	points = list(filter(lambda d: d['mean'] != None, copy_data))
	nullPoints = list(filter(lambda d: d['mean'] == None, copy_data))

	if len(points) < 3:
		return nullPoints
	m0 = len(points)
	m1 = len(nullPoints)

	r = []

	for i in range(m1):
		for j in range(m0):
			tmpDis = distanceByLnglat(nullPoints[i]['lat'], nullPoints[i]['lng'], points[j]['lat'], points[j]['lng'])
			r.append(tmpDis)

	for i in range(m1):
		ifFind = False
		for j in range(m0*i, m0*i+m0):
			if abs(r[j]) < 10:
				nullPoints[i]['mean'] = points[j - m0 * i]['mean']
				nullPoints[i]['variance'] = points[j - m0 * i]['variance']
				nullPoints[i]['max'] = points[j - m0 * i]['max']
				nullPoints[i]['std'] = points[j - m0 * i]['std']
				ifFind = True
				break
		if ifFind:
			continue
		
		numerator = 0
		numerator1= 0
		numerator2= 0
		numerator3= 0

		denominator = 0
		for j in range(m0*i, m0*i+m0):
			numerator += (points[j - m0 * i]['mean'] / (r[j] * r[j]))
			numerator1 += (points[j - m0 * i]['variance'] / (r[j] * r[j]))
			numerator2 += (points[j - m0 * i]['max'] / (r[j] * r[j]))
			numerator3 += (points[j - m0 * i]['std'] / (r[j] * r[j]))
			denominator += (1 / (r[j] * r[j]))
		nullPoints[i]['mean'] = numerator / denominator
		nullPoints[i]['variance'] = numerator1 / denominator
		nullPoints[i]['max'] = numerator2 / denominator
		nullPoints[i]['std'] = numerator3 / denominator
	
	return points + nullPoints

def initDim2Arr(m, n):
	dim2Arr = []
	for i in range(m):
		row = []
		for j in range(n):
			row.append({'list': []})
		dim2Arr.append(row)
	return dim2Arr

def scale(domain, range, value):
	span_num = (domain[1] - domain[0]) / (range[1] - range[0])
	return math.floor((value - domain[0]) / span_num)

def add_grid_info(origin_data):

	dim2Arr = initDim2Arr(m, n)

	for d in origin_data:
		x = scale([left, right], [0, n], d['longitude'])
		y = scale([bottom, top], [0, m], d['latitude'])

		dim2Arr[m-1-y][x]['list'].append(d['value'])

	griddata = []
	for i in range(m):
		for j in range(n):
			lngEx = [left + j*span, left + (j+1)*span]
			latEx = [top - (i+1)*span, top - i*span]
			mean, variance, std, maxValue = None, None, None, None
			flag = False
			if len(dim2Arr[i][j]['list']) > 0:
				mean = np.mean(dim2Arr[i][j]['list'])
				variance = np.var(dim2Arr[i][j]['list'])
				std = math.sqrt(variance)
				maxValue = max(dim2Arr[i][j]['list'])
				flag = True
			obj = {'i':i, 'j':j, 'lat': np.mean(latEx), 'lng': np.mean(lngEx), 'latEx': latEx, 'lngEx': lngEx, 'max': maxValue, 'std':std, 'mean': mean, 'variance': variance, 'flag': flag}
			griddata.append(obj)

	return griddata

def getLastPointsInGrid(origin_data):
	""" 计算每个格子中最后一个sid的点的位置
	"""
	dic = {}
	data= []
	for d in origin_data:
		x = scale([left, right], [0, n], d['longitude'])
		y = scale([bottom, top], [0, m], d['latitude'])
		xy_str = str(m-1-y)+','+str(x)
		if xy_str not in dic.keys():
			dic[xy_str] = {}
		dic[xy_str] = {'time': d['timestamp'], 'longitude': d['longitude'], 'latitude': d['latitude']}
	for k, v in dic.items():
		data.append({'xy': k, 'time':v['time'], 'longitude': v['longitude'], 'latitude': v['latitude']})
	return data

if __name__ == "__main__":
	params = {'begintime': '2020-04-08 17:46:03', 'endtime': '2020-04-08 18:46:13'}
	cursor = connection.cursor()
	cursor.execute("select longitude, latitude, value from mobilesensorreadings where timestamp > '{0}'  and timestamp < '{1}'".format(params['begintime'], params['endtime']))
	desc = cursor.description
	alldata = cursor.fetchall()
	data = [dict(zip([col[0] for col in desc], row)) for row in alldata]
	griddata = add_grid_info(data)

	idwdata = idw(griddata)
	print(idwdata)

	# params = {'begintime': '2020-04-08 17:46:03', 'endtime': '2020-04-08 18:46:13'}
	# cursor = connection.cursor()
	# cursor.execute("select longitude, latitude, sid from mobilesensorreadings where timestamp > '{0}'  and timestamp < '{1}'".format(params['begintime'], params['endtime']))
	# desc = cursor.description
	# alldata = cursor.fetchall()
	# origin_data = [dict(zip([col[0] for col in desc], row)) for row in alldata]
	# data = getLastPointInGrid(origin_data)
	# print(data)
	# print(len(data))

	


