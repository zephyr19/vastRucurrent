# -*- coding: utf-8 -*-
import sys
import os
import django
import json
from django.db import connection
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.manifold import TSNE
from sklearn.preprocessing import RobustScaler
from scipy import stats
import math
from sklearn.manifold import MDS
from sklearn.cluster import DBSCAN
import math
import datetime, time
import logging

# 找到项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RadiationVis.settings')
django.setup()

from backend.models import MobileSensorReadings
from backend.models import StaticSensorReadings

logger = logging.getLogger(__name__)
'''
    使用空缺值之前的四个值的均值进行补全
'''
def Matrix_Completion_1(m):

    index = np.argwhere(np.isnan(m))
    [rows1, cols1] = index.shape
    for i in range(rows1):
        # tmp = m[index[i,0],index[i,1]]
        if i < 1:
            m[index[i, 0], index[i, 1]] = 0
        elif i < 4:
            m[index[i, 0], index[i, 1]] = m[index[i, 0] - 1, index[i, 1]]
        else:
            m[index[i, 0], index[i, 1]] = 0.25 * (
                m[index[i, 0] - 1, index[i, 1]] + m[index[i, 0] - 2, index[i, 1]] + m[index[i, 0] - 3, index[i, 1]] + m[
                    index[i, 0] - 4, index[i, 1]])
    return m


'''
    使用 -200 代替 Nan
'''
def Matrix_Completion_2(m):

    index = np.argwhere(np.isnan(m))
    [rows1, cols1] = index.shape
    for i in range(rows1):
        m[index[i, 0], index[i, 1]] = -200
    return m

'''
    欧式距离
'''
def Distance_Metric_Euclidean(m):
    feature_matrix = np.eye(59)
    [rows2, cols2] = feature_matrix.shape
    for i in range(rows2):
        for j in range(cols2):
            tmp1 = m[:, i].T.tolist()
            tmp2 = m[:, j].T.tolist()

            numerator = np.sqrt(sum([(a - b) ** 2 for (a, b) in zip(tmp1, tmp2)]))

            feature_matrix[i, j] = numerator

    return feature_matrix

'''
    余弦距离
'''
def Distance_Metric_Cos(m, 	sensor_length):
    feature_matrix = np.eye(sensor_length)
    [rows2, cols2] = feature_matrix.shape
    for i in range(rows2):
        for j in range(cols2):
            tmp1 = m[:, i].T.tolist()
            tmp2 = m[:, j].T.tolist()

            numerator = sum([(a * b) for (a, b) in zip(tmp1, tmp2)])
            sq1 = np.sqrt(sum([np.power(e, 2) for e in tmp1]))
            sq2 = np.sqrt(sum([np.power(e, 2) for e in tmp2]))
            denominator = sq1 * sq2
            ac = numerator * 1.0 / denominator

            feature_matrix[i, j] = ac
    return feature_matrix

'''减弱异常'''
def Centralized_with_Outliers(m):
    transformer = RobustScaler().fit(m)
    return transformer.transform(m)



def Dimension_Reduction_MDS(feature_matrix):
    mds = MDS(n_components=2).fit_transform(feature_matrix)
    [m, n] = mds.shape
    return mds



'''降维方法： TSNE'''
def Dimension_Reduction_TSNE(feature_matrix):
    tsne = TSNE(n_components=2, n_iter=3000).fit_transform(feature_matrix)
    [m,n] = tsne.shape
    # print(m, n)

    return tsne

def Cluster_DBSCAN(result, jitter_result):
    [m,n] = result.shape
    cluster_res = DBSCAN().fit_predict(result)
    return cluster_res

def Jitter(series, factor):
    z = float(series.max()) - float(series.min())
    a = float(factor) * z / 50.
    for i in range(len(series)):
        series[i] = series[i] + np.random.uniform(-a, a)
    return series
    # return series.apply(lambda x: x + np.random.uniform(-a, a))


def calCorrlelation(begintime, endtime):
	'''
	load mobile sensor
	'''
	cursor = connection.cursor()
	cursor.execute("select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value) from mobilesensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(begintime, endtime))
	alldata = cursor.fetchall()
	data = []
	sensors1 = set()
	for i in alldata:
		data.append({'time': i[0], 'sid': i[1], 'value': i[2]})
		sensors1.add(i[1])
	sensors_title1 = set()
	for i in sensors1:
		str1 = 'm' + str(i)
		sensors_title1.add(str1)
	sensors_title1 = list(sensors_title1)
	# begin = datetime.date(2020, 4, 6)
	# end = datetime.date(2020, 4, 11)
	begin = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
	end = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
	begin_timestamp = time.mktime(begin.timetuple())
	end_timestamp = time.mktime((end.timetuple()))
	current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
	obs1 = {}
	while current <= end_timestamp:
		date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
		obs1[date_str] = {}
		for i in list(sensors1):
			obs1[date_str][i] = math.nan
		current += 3600
	# print(obs)
	for d in data:
		obs1[d['time']][d['sid']] = d['value']

	# print(obs)
	# for obs1 in obs.values():
	# 	print(len(obs1))
	tmp = []
	obs_len=len(obs1)
	for value in obs1.values():
		tmp.append(list(value.values()))
	m = np.array(tmp[0])
	for i in range(1,obs_len):
		t = np.array(tmp[i])
		m = np.vstack((m, t)) # 120 * 50

	'''
		load staticsensor
	'''
	cursor = connection.cursor()
	cursor.execute("select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(begintime, endtime))
	alldata = cursor.fetchall()
	data = []
	sensors2 = set()
	for i in alldata:
		data.append({'time': i[0], 'sid': i[1], 'value': i[2]})
		sensors2.add(i[1])
	sensors_title2 = set()
	for i in sensors2:
		str2 = 's' + str(i)
		sensors_title2.add(str2)
	sensors_title2 = list(sensors_title2)
	sensors_title = sensors_title1 + sensors_title2
	sensor_length = len(sensors_title)
# begin = datetime.date(2020, 4, 6)
	# end = datetime.date(2020, 4, 11)
	# begin_timestamp = time.mktime(begin.timetuple())
	# end_timestamp = time.mktime((end.timetuple()))
	current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
	obs2 = {}
	while current <= end_timestamp:
		date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
		obs2[date_str] = {}
		for i in list(sensors2):
			obs2[date_str][i] = math.nan
		current += 3600
	for d in data:
		obs2[d['time']][d['sid']] = d['value']
	tmp = []
	obs_len = len(obs2)
	for value in obs2.values():
		tmp.append(list(value.values()))
	n = np.array(tmp[0])
	for i in range(1, obs_len):
		t = np.array(tmp[i])
		n = np.vstack((n, t))  # 120 * 50

	mn = np.hstack((m, n))

	'''
	        不确定性指标
	    '''
	col_mean = np.nanmean(mn, axis=0).tolist()  # 均值
	index_col = np.argwhere(np.isnan(col_mean))
	if len(index_col) > 0:
		for i in range(len(index_col)):
			col_mean[index_col[i][0]] = 0
	mn = Matrix_Completion_2(mn)
	[a, b] = mn.shape
	
	# col_std = np.std(mn, axis=0).tolist()  # 标准差
	# col_sem = []  # 标准误
	# for i in range(b):
	# 	col_sem.append(col_std[i] / math.sqrt(a))
	# col_max = mn.max(axis=0)
	# col_min = mn.min(axis=0)
	# col_distance = (col_max - col_min).tolist()  # 范围 max-min
	# # print(col_distance)
	# col_confidence_interval = []  # 95%置信区间
	# for i in range(b):
	# 	col_confidence_interval.append(stats.norm.interval(0.95, col_mean[i], col_std[i]))
	# # print(col_confidence_interval)

	feature_matrix = Distance_Metric_Cos(mn, sensor_length)

	result = Dimension_Reduction_MDS(feature_matrix)  # 降维
	'''
    聚类： 每类标不同颜色
    '''

	[a, b] = result.shape
	# print(a,b )
	col_x = result[:, 0]
	col_y = result[:, 1]

	'''
    添加抖动： 按列抖动，设置抖动因子
    '''
	jitter_factor = 50
	jitter_col_x = Jitter(col_x, jitter_factor)
	jitter_col_y = Jitter(col_y, jitter_factor)
	jitter_result = np.vstack((jitter_col_x, jitter_col_y))
	jitter_result = jitter_result.T

	# Draw_plot(jitter_result)
	# print(jitter_result)
	cluster = Cluster_DBSCAN(result, jitter_result)
	detectorS = []
	i = 0
	for data in result:
		detectorS.append(
			{'id':sensors_title[i], 'x': data[0], 'y': data[1], 'mean': col_mean[i]})
		i = i + 1
	return detectorS

if __name__ == '__main__':
	# timestr = '2020-04-09 20:00:00'
	# d = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
	# print(time.mktime(d.timetuple()))\
	calCorrlelation('2020-04-06 00:00:00', '2020-04-06 01:00:00')