# coding=utf-8
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import sys
import os
import django
import json
from django.db import connection
from datetime import datetime
from sklearn.manifold import TSNE
from sklearn.preprocessing import RobustScaler
from scipy import stats
import math
from sklearn.manifold import MDS
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import datetime, time
import logging
import scipy.io as sio

# 找到项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RadiationVis.settings')
django.setup()

from backend.models import MobileSensorReadings
from backend.models import StaticSensorReadings

logger = logging.getLogger(__name__)

class ToolFuncOfDTW:
    def __init__(self):
        pass

    # @staticmethod
    # def print_matrix(mat):
    #     print('[matrix] width : %d height : %d' % (len(mat[0]), len(mat)))
    #     print('-----------------------------------')
    #     for i in range(len(mat)):
    #         print(mat[i])  # [v[:2] for v in mat[i]]


class DTW:

    def __init__(self):
        pass

    @staticmethod
    def numpy_num_to_python_num(p1):
        if isinstance(p1, np.int32):
            p1 = int(p1)
        elif isinstance(p1, np.float64):
            p1 = float(p1)
        return p1

    @staticmethod
    def dist_for_float(p1, p2):
        p1 = DTW.numpy_num_to_python_num(p1)
        p2 = DTW.numpy_num_to_python_num(p2)
        if (type(p1) == float or type(p1) == int) and \
                (type(p2) == float or type(p2) == int):
            dist = float(abs(p1 - p2))
            return dist
        else:
            sum_val = 0.0
            for i in range(len(p1)):
                sum_val += pow(p1[i] - p2[i], 2)
            dist = pow(sum_val, 0.5)
            return dist

    @staticmethod
    def dtw(s1, s2, dist_func):
        w = len(s1)
        h = len(s2)

        mat = [([[0, 0, 0, 0*j*i] for j in range(w)]) for i in range(h)]

        for x in range(w):
            for y in range(h):
                dist = dist_func(s1[x], s2[y])
                mat[y][x] = [dist, 0, 0, 0]
                # DTW.print_matrix(mat)

        elem_0_0 = mat[0][0]
        elem_0_0[1] = elem_0_0[0] * 2

        for x in range(1, w):
            mat[0][x][1] = mat[0][x][0] + mat[0][x - 1][1]
            mat[0][x][2] = x - 1
            mat[0][x][3] = 0

        for y in range(1, h):
            mat[y][0][1] = mat[y][0][0] + mat[y - 1][0][1]
            mat[y][0][2] = 0
            mat[y][0][3] = y - 1

        for y in range(1, h):
            for x in range(1, w):
                distlist = [mat[y][x - 1][1], mat[y - 1][x][1], 2 * mat[y - 1][x - 1][1]]
                mindist = min(distlist)
                idx = distlist.index(mindist)
                mat[y][x][1] = mat[y][x][0] + mindist
                if idx == 0:
                    mat[y][x][2] = x - 1
                    mat[y][x][3] = y
                elif idx == 1:
                    mat[y][x][2] = x
                    mat[y][x][3] = y - 1
                else:
                    mat[y][x][2] = x - 1
                    mat[y][x][3] = y - 1

        result = mat[h - 1][w - 1]
        retval = result[1]
        path = [(w - 1, h - 1)]
        while True:
            x = result[2]
            y = result[3]
            path.append((x, y))

            result = mat[y][x]
            if x == 0 and y == 0:
                # DTW.print_matrix(mat)
                break
        return retval, sorted(path)

    @staticmethod
    def distance(s1, s2, signal_num=-9999):
        # type: (np.ndarray, np.ndarray, int) -> float
        tmp_s1 = []
        for i in s1:
            tmp_s1.append(i)
        tmp_s2 = []
        for i in s2:
            tmp_s2.append(i)
        s1_in = DTW.return_center_data(tmp_s1, signal_num)
        s2_in = DTW.return_center_data(tmp_s2, signal_num)
        result = DTW.dtw(s1_in, s2_in, DTW.dist_for_float)[0]
        # print(result, s1_in, s2_in)
        return result

    @staticmethod
    def return_center_data(list_data, signal_num=-9999):
        # type: (list, int) -> list
        start = 0
        end = len(list_data)
        for i in range(len(list_data)):
            if list_data[i] != signal_num:
                start = i
                break

        for i in range(len(list_data)-1, 0, -1):
            if list_data[i] != signal_num:
                end = i + 1
                break
        return list_data[start:end]


class TestDTW:

    def __init__(self):
        pass

    @staticmethod
    def display(s1, s2):
        val, path = DTW.dtw(s1, s2, DTW.dist_for_float)

        w = len(s1)
        h = len(s2)

        mat = [[1] * (w + 0*i) for i in range(h)]
        for node in path:
            x, y = node
            mat[y][x] = 0

        mat = np.array(mat)

        plt.subplot(2, 2, 2)
        plt.pcolor(mat, edgecolors='k', linewidths=4)
        # print(c)
        plt.title('Dynamic Time Warping (%f)' % val)

        plt.subplot(2, 2, 1)
        plt.plot(s2, range(len(s2)), 'g')

        plt.subplot(2, 2, 4)
        plt.plot(range(len(s1)), s1, 'r')

        plt.show()

    @staticmethod
    def test_path():
        s1 = [1, 2, 3, 4, 5, 5, 5, 4]
        s2 = [3, 4, 5, 5, 5, 4]
        # s2 = s1
        # s2 = [1, 2, 3, 4, 5, 5]
        # s2 = [2, 3, 4, 5, 5, 5]
        val, path = DTW.dtw(s1, s2, DTW.dist_for_float)
        TestDTW.display(s1, s2)
        print(val, path)

    @staticmethod
    def test_remove_signal():
        s1 = [1, 2, 3, 4, 5, -9999, -9999, -9999, -9999, -9999]
        s2 = [-9999, -9999, -9999, 1, 2, 3, 4, 5, -9999, -9999, -9999, -9999, -9999]
        # print(np.array(s1), type(np.array(s1)))
        result = DTW.distance(np.array(s1), np.array(s2))
        TestDTW.display(s1, s2)
        # print(s1)
        # print(s2)
        # print(result)

    @staticmethod
    def test_cluster_effect():
        from sklearn.neighbors import NearestNeighbors
        LL = 3

        def d(a, b, l):
            # type: (np.ndarray, np.ndarray, int) -> float
            # print(sum(a.tolist()))
            aa = a.tolist()  # 返回的是可迭代对象，不是list
            bb = b.tolist()
            # print(aa, type(aa))
            # print(bb, type(bb))
            result_d = 0.0

            tmp_list_a = []
            for i in aa:
                tmp_list_a.append(i)

            tmp_list_b = []
            for i in bb:
                tmp_list_b.append(i)

            for i in range(len(tmp_list_b)):
                result_d += (tmp_list_a[i] - tmp_list_b[i])*(tmp_list_a[i] - tmp_list_b[i])
            # print(type(a))
            # print(type(b))
            # result_d = bb + aa + float(2 + L)
            # bb += aa
            # result_d = bb
            return result_d + l

        knn = NearestNeighbors(n_neighbors=2,
                               algorithm='auto',
                               metric=lambda a, b: d(a, b, LL)
                               )
        # X = pd.DataFrame({'b': [0, 3, 2], 'c': [1.0, 4.3, 2.2]})
        X = np.array([[-1, -1],
                      [-2, -1],
                      [-3, -2],
                      [1, 1],
                      [2, 1],
                      [3, 2]])
        knn.fit(X)
        # result = knn.predict([0, 3, 1.9])
        distances, indices = knn.kneighbors(X)
        # print(distances)
        # print(indices)
        # print(knn.kneighbors_graph(X).toarray())
        # print("---------------------------")
        # distances, indices = knn.kneighbors(np.array([[-3, -3]]))
        # print(distances)
        # print(indices)
        # print(knn.kneighbors_graph(X).toarray())

    @staticmethod
    def test_cluster_effect_agg():
        s = [[1, 2, 3, 11, 11, 6, 6, 6, 6, -9999, -9999, -9999, -9999],
             [-9999, -9999, -9999, 2, 2, 3, 11, 4, 6, 6, 6, 7, -9999],
             [3, 8, 3, 1, 2, 3, 3, -9999, -9999, -9999, -9999, -9999, -9999],
             [4, 8, 3, 1, 2, 3, 4, -9999, -9999, -9999, -9999, -9999, -9999],
             [-9999, -9999, 5, 8, 3, 1, 2, 3, 3, 4,  -9999, -9999, -9999]]
        X = np.array(s)
        dbscan = DBSCAN(eps=14,
                        min_samples=2,
                        metric=lambda a, b: DTW.distance(a, b))  # 可以自定义距离函数
        cluster = dbscan.fit_predict(X)
        
        plt.rcParams.update({'figure.autolayout': True})
        for i in range(len(s)):
            size = (len(s)+1)*100 + 10 + (i+1)
            plt.subplot(size)
            plt.plot(DTW.return_center_data(s[i]))  # , title='title'+str(i)
            plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8])
            plt.ylabel(str(i+1))
        plt.xlabel('step')
        plt.show()

    @staticmethod
    def Matrix_Completion_2(m):
        index = np.argwhere(np.isnan(m))
        [rows1, cols1] = index.shape
        for i in range(rows1):
            m[index[i, 0], index[i, 1]] = -9999
        return m

    @staticmethod
    def Matrix_Completion_3(m):
        index = np.argwhere(np.isnan(m))
        [rows1, cols1] = index.shape
        for i in range(rows1):
            m[index[i, 0], index[i, 1]] = 0
        return m

    @staticmethod
    def Matrix_Completion_4(m):
        index = np.argwhere(np.isnan(m))
        [rows1, cols1] = index.shape
        for i in range(rows1):
            m[index[i, 0], index[i, 1]] = -1
        return m

    @staticmethod
    def Distance_Metric_Cos(m, sensor_len):
        feature_matrix = np.eye(sensor_len)
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

    @staticmethod
    def Dimension_Reduction_PCA(feature_matrix):
        pca = PCA(n_components=2)
        pca = pca.fit_transform(feature_matrix)
        return pca

    @staticmethod
    def Cluster_DBSCAN(result):
        [m, n] = result.shape
        cluster_res = DBSCAN(eps=0.8, min_samples=2).fit_predict(result)
        return cluster_res

    @staticmethod
    def static_mobile_cluster(begintime, endtime):
        begin_date = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        begin_timestamp = time.mktime(begin_date.timetuple())
        end_timestamp = time.mktime(end_date.timetuple())
        cursor = connection.cursor()
        inconsistency_data = [
            11.81,
            12.51,
            6.70,
            0.85,
            0.80,
            6.90,
            2.68,
            3.90,
            3.77,
            1.65,
            4.20,
            3.93,
            2.02,
            1.52,
            0.54,
            1.67,
            19.05,
            22.52,
            8.18,
            27.36,
            19.71,
            5.03,
            1.21,
            9.07,
            13.21,
            18.61,
            10.16,
            0.53,
            0.72,
            1.21,
            0.96,
            15.27,
            14.93,
            16.20,
            16.31,
            26.59,
            6.37,
            27.33,
            26.84,
            18.59,
            16.48,
            20.10,
            18.50,
            27.22,
            24.62,
            25.92,
            24.46,
            27.05,
            27.18,
            20.80
        ]
        # if (end_timestamp - begin_timestamp) > 48 * 3600:
        #     cursor.execute(
        #         "select CONCAT(DATE_FORMAT(`timestamp`, '%Y-%m-%d '),LPAD(	FLOOR(DATE_FORMAT(`timestamp`, '%H') / 3) * 3,2,'0'),':00'), sid, avg(value) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY CONCAT(DATE_FORMAT(`timestamp`, '%Y-%m-%d '),LPAD(	FLOOR(DATE_FORMAT(`timestamp`, '%H') / 3) * 3,2,'0'),':00')".format(
        #             begintime, endtime))
        #     alldata = cursor.fetchall()
        #     data = []
        #     mobile_sensors = set()
        #     for i in alldata:
        #         data.append({'time': i[0], 'sid': i[1], 'value': i[2]})
        #         mobile_sensors.add(i[1])
        #     mobile_sensors = list(mobile_sensors)
        #     begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M')
        #     end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M')
        #     begin_timestamp = time.mktime(begin.timetuple())
        #     end_timestamp = time.mktime((end.timetuple()))
        #     current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M').timetuple())
        #     obs1 = {}
        #     while current <= end_timestamp:
        #         date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
        #         obs1[date_str] = {}
        #         for i in mobile_sensors:
        #             obs1[date_str][i] = math.nan
        #         current += 10800
        #     for d in data:
        #         obs1[d['time']][d['sid']] = d['value']
        #     tmp = []
        #     obs_len = len(obs1)
        #     for value in obs1.values():
        #         tmp.append(list(value.values()))
        #     m = np.array(tmp[0])
        #     for i in range(1, obs_len):
        #         t = np.array(tmp[i])
        #         m = np.vstack((m, t))  # 120 * 50

        if (end_timestamp - begin_timestamp) > 6 * 3600:
        # elif ((end_timestamp - begin_timestamp)) > 3 * 3600 and (end_timestamp - begin_timestamp) <= 48 * 3600:
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value), AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from mobilesensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            mobile_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                mobile_sensors.add(i[1])
            mobile_sensors = list(mobile_sensors)
            begin = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs1 = {}
            mobile_sensors_all = []
            for i in range(1,51):
                mobile_sensors_all.append(i)

            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs1[date_str] = {}
                for i in mobile_sensors:
                    obs1[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs1[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs1_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs1_accuracy[date_str] = {}
                for i in mobile_sensors:
                    obs1_accuracy[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs1_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs1_accuracy)
            for value in obs1_accuracy.values():
                tmp.append(list(value.values()))
            m_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                m_accuracy = np.vstack((m_accuracy, t))  # 120 * 50


            tmp = []
            obs_len = len(obs1)
            for value in obs1.values():
                tmp.append(list(value.values()))
            m = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                m = np.vstack((m, t))  # 120 * 50
            
        else:
            cursor.execute(
                '''select DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE), sid, avg(value), AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from mobilesensorreadings where timestamp between '{}' and '{}' GROUP BY DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE),sid'''.format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            mobile_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2],'accuracy': round(i[3])})
                mobile_sensors.add(i[1])
            mobile_sensors_all = []


            for i in range(1, 51):
                mobile_sensors_all.append(i)
            mobile_sensors = list(mobile_sensors)
            begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs1 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs1[date_str] = {}
                for i in mobile_sensors:
                    obs1[date_str][i] = math.nan
                current += 600
            for d in data:
                obs1[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs1_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs1_accuracy[date_str] = {}
                for i in mobile_sensors:
                    obs1_accuracy[date_str][i] = math.nan
                current += 600
            for d in data:
                obs1_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs1_accuracy)
            for value in obs1_accuracy.values():
                tmp.append(list(value.values()))
            m_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                m_accuracy = np.vstack((m_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs1)
            for value in obs1.values():
                tmp.append(list(value.values()))
            m = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                m = np.vstack((m, t))  # 120 * 50
            

        '''
            load staticsensor
        '''
        cursor = connection.cursor()
        # if (end_timestamp - begin_timestamp) > 48 * 3600:
        #     cursor.execute(
        #         "select CONCAT(DATE_FORMAT(`timestamp`, '%Y-%m-%d '),LPAD(	FLOOR(DATE_FORMAT(`timestamp`, '%H') / 3) * 3,2,'0'),':00'), sid, avg(value) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY CONCAT(DATE_FORMAT(`timestamp`, '%Y-%m-%d '),LPAD(	FLOOR(DATE_FORMAT(`timestamp`, '%H') / 3) * 3,2,'0'),':00')".format(
        #             begintime, endtime))
        #     alldata = cursor.fetchall()
        #     data = []
        #     static_sensors = set()
        #     for i in alldata:
        #         data.append({'time': i[0], 'sid': i[1], 'value': i[2]})
        #         static_sensors.add(i[1])
        #     static_sensors = list(static_sensors)
        #     sensors_title = [('m' + str(i)) for i in mobile_sensors] + [('s' + str(j)) for j in static_sensors]
        #     sensor_length = len(sensors_title)
        #
        #     begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M')
        #     end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M')
        #     begin_timestamp = time.mktime(begin.timetuple())
        #     end_timestamp = time.mktime((end.timetuple()))
        #     current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M').timetuple())
        #     obs2 = {}
        #     while current <= end_timestamp:
        #         date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
        #         obs2[date_str] = {}
        #         for i in static_sensors:
        #             obs2[date_str][i] = math.nan
        #         current += 10800
        #     for d in data:
        #         obs2[d['time']][d['sid']] = d['value']
        #     tmp = []
        #     obs_len = len(obs2)
        #     for value in obs2.values():
        #         tmp.append(list(value.values()))
        #     n = np.array(tmp[0])
        #     for i in range(1, obs_len):
        #         t = np.array(tmp[i])
        #         n = np.vstack((n, t))  # 120 * 50

        if (end_timestamp - begin_timestamp) > 6 * 3600:
        # elif ((end_timestamp - begin_timestamp) > 3 * 3600) and (end_timestamp - begin_timestamp) <= 48 * 3600:
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value),AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            static_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                static_sensors.add(i[1])
            static_sensors = list(static_sensors)

            static_sensors_all = [1,4,6,9,11,12,13,14,15]

            begin = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)
            end = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs2 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs2[date_str] = {}
                for i in static_sensors:
                    obs2[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs2[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs2_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs2_accuracy[date_str] = {}
                for i in static_sensors:
                    obs2_accuracy[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs2_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs2_accuracy)
            for value in obs2_accuracy.values():
                tmp.append(list(value.values()))
            n_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                n_accuracy = np.vstack((n_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs2)
            for value in obs2.values():
                tmp.append(list(value.values()))
            n = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                n = np.vstack((n, t))  # 120 * 50
            
        else:
            cursor.execute(
                '''select DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE), sid, avg(value),AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE),sid'''.format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            static_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                static_sensors.add(i[1])
            static_sensors = list(static_sensors)
            static_sensors_all = [1,4,6,9,11,12,13,14,15]
            begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs2 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs2[date_str] = {}
                for i in static_sensors:
                    obs2[date_str][i] = math.nan
                current += 600
            for d in data:
                obs2[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs2_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs2_accuracy[date_str] = {}
                for i in static_sensors:
                    obs2_accuracy[date_str][i] = math.nan
                current += 600
            for d in data:
                obs2_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs2_accuracy)
            for value in obs2_accuracy.values():
                tmp.append(list(value.values()))
            n_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                n_accuracy = np.vstack((n_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs2)
            for value in obs2.values():
                tmp.append(list(value.values()))
            n = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                n = np.vstack((n, t))  # 120 * 50

        sensor_length_all = 59
        sensors_title_all = [('m' + str(i)) for i in mobile_sensors_all] + [('s' + str(j)) for j in static_sensors_all]
        sensors_title = [('m' + str(i)) for i in mobile_sensors] + [('s' + str(j)) for j in static_sensors]
        sensor_len = len(sensors_title)

        mn = np.hstack((m, n))
        mn_accuracy = np.hstack((m_accuracy, n_accuracy))

        '''
        不确定性指标计算
        '''
        index_nan_mn = np.argwhere(np.isnan(mn))
        nan_col = index_nan_mn[:,1]
        uniques = np.unique(nan_col)
        nan_result = []
        for i in set(nan_col):
            nan_result.append(nan_col.tolist().count(i))
        # print(nan_result)
        # print(len(nan_result))
        # print(len(uniques))
        col_nan = np.zeros(sensor_len)
        for i in range(len(col_nan)):
            for j in range(len(uniques)):
                col_nan[uniques[j]] = nan_result[j]

        # mn_accuracy = TestDTW.Matrix_Completion_4(mn_accuracy)
        [a,b] = mn_accuracy.shape
        mn_accuracy_count = np.nanmean(mn_accuracy, axis = 0)
        mn_accuracy_count = np.around(mn_accuracy_count).tolist()

        col_mean = np.nanmean(mn, axis=0).tolist()  # 均值
        col_std = np.nanstd(mn, axis=0).tolist()  # 标准差
        index_col = np.argwhere(np.isnan(col_mean))
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_mean[index_col[i][0]] = 0
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_std[index_col[i][0]] = 0

        #不一致性衡量
        sl = len(static_sensors)
        col_inconsistency = {}
        for i in range(len(inconsistency_data)):
            if i+1 in mobile_sensors:
                col_inconsistency[i+1] = inconsistency_data[i]
        col_inconsistency = list(col_inconsistency.values())
        col_inconsistency = col_inconsistency + [0] * sl


        if (end_timestamp - begin_timestamp) > 48 * 3600:
            mn = TestDTW.Matrix_Completion_3(mn)
            # mn = Centralized_with_Outliers(mn)
            [a, b] = mn.shape

            result = TestDTW.Distance_Metric_Cos(mn, sensor_len)
            result = TestDTW.Dimension_Reduction_PCA(result)

            # result = Dimension_Reduction_MDS(feature_matrix)  # 降维
            '''
            聚类： 每类标不同颜色
            '''

            cluster = TestDTW.Cluster_DBSCAN(result)
            cluster_label = cluster.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)


            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all


            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster":cluster_label[i],"mean":col_mean[i],"std":col_std[i], "nan":col_nan[i]/a, "accuracy":mn_accuracy_count[i], "inconsistency": col_inconsistency[i]}
            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
                    col_inconsistency_all[i] = have_value_sensors[sensors_title_all[i]]["inconsistency"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type


            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],"nan":col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency": col_inconsistency_all[i]})
            
            return tree
        else:
            mn = mn.T
            mn = TestDTW.Matrix_Completion_2(mn)
            [a,b] = mn.shape
            dbscan = DBSCAN(eps=35,
                            min_samples=2,
                            metric=lambda a, b: DTW.distance(a, b))  # 可以自定义距离函数
            cluster_label = dbscan.fit_predict(mn)
            # print(cluster_label)

            cluster_label = cluster_label.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)

            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all

            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster": cluster_label[i], "mean": col_mean[i],
                                                        "std": col_std[i], "nan": col_nan[i] / a,
                                                        "accuracy": mn_accuracy_count[i],
                                                        "inconsistency": col_inconsistency[i]}
            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
                    col_inconsistency_all[i] = have_value_sensors[sensors_title_all[i]]["inconsistency"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type

            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],
                     "nan": col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency": col_inconsistency_all[i]})
            
            return tree

    @staticmethod
    def static_cluster(begintime, endtime):
        begin_date = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        begin_timestamp = time.mktime(begin_date.timetuple())
        end_timestamp = time.mktime(end_date.timetuple())

        '''
            load staticsensor
        '''
        cursor = connection.cursor()
        if (end_timestamp - begin_timestamp) > 6 * 3600:
        # elif ((end_timestamp - begin_timestamp) > 3 * 3600) and (end_timestamp - begin_timestamp) <= 48 * 3600:
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value),AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            static_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                static_sensors.add(i[1])
            static_sensors = list(static_sensors)

            static_sensors_all = [1, 4, 6, 9, 11, 12, 13, 14, 15]

            begin = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)
            end = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs2 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs2[date_str] = {}
                for i in static_sensors:
                    obs2[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs2[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs2_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs2_accuracy[date_str] = {}
                for i in static_sensors:
                    obs2_accuracy[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs2_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs2_accuracy)
            for value in obs2_accuracy.values():
                tmp.append(list(value.values()))
            n_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                n_accuracy = np.vstack((n_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs2)
            for value in obs2.values():
                tmp.append(list(value.values()))
            n = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                n = np.vstack((n, t))  # 120 * 50
            
        else:
            cursor.execute(
                '''select DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE), sid, avg(value),AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from staticsensorreadings where timestamp between '{}' and '{}' GROUP BY DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE),sid'''.format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            static_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                static_sensors.add(i[1])
            static_sensors = list(static_sensors)
            static_sensors_all = [1, 4, 6, 9, 11, 12, 13, 14, 15]
            begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs2 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs2[date_str] = {}
                for i in static_sensors:
                    obs2[date_str][i] = math.nan
                current += 600
            for d in data:
                obs2[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs2_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs2_accuracy[date_str] = {}
                for i in static_sensors:
                    obs2_accuracy[date_str][i] = math.nan
                current += 600
            for d in data:
                obs2_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs2_accuracy)
            for value in obs2_accuracy.values():
                tmp.append(list(value.values()))
            n_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                n_accuracy = np.vstack((n_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs2)
            for value in obs2.values():
                tmp.append(list(value.values()))
            n = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                n = np.vstack((n, t))  # 120 * 50

        sensor_length_all = 9
        sensors_title_all = [('s' + str(j)) for j in static_sensors_all]
        sensors_title = [('s' + str(j)) for j in static_sensors]
        sensor_len = len(sensors_title)
        mn = n
        mn_accuracy = n_accuracy
        # print(mn)
        '''
        不确定性指标计算
        '''
        index_nan_mn = np.argwhere(np.isnan(mn))
        nan_col = index_nan_mn[:, 1]
        uniques = np.unique(nan_col)
        nan_result = []
        for i in set(nan_col):
            nan_result.append(nan_col.tolist().count(i))
        # print(nan_result)
        # print(len(nan_result))
        # print(len(uniques))
        col_nan = np.zeros(sensor_len)
        for i in range(len(col_nan)):
            for j in range(len(uniques)):
                col_nan[uniques[j]] = nan_result[j]

        # mn_accuracy = TestDTW.Matrix_Completion_4(mn_accuracy)
        [a, b] = mn_accuracy.shape
        mn_accuracy_count = np.nanmean(mn_accuracy, axis=0)
        mn_accuracy_count = np.around(mn_accuracy_count).tolist()
        print(mn_accuracy_count)
        # mn_accuracy_count = []
        # [a, b] = mn_accuracy.shape
        # for i in range(b):
        #     tmp = np.unique(mn_accuracy[:, i])
        #     print(tmp)
        #     mn_accuracy_count.append(len(tmp))
        # print(mn_accuracy_count)
        # print(len(mn_accuracy_count))

        col_mean = np.nanmean(mn, axis=0).tolist()  # 均值
        col_std = np.nanstd(mn, axis=0).tolist()  # 标准差
        index_col = np.argwhere(np.isnan(col_mean))
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_mean[index_col[i][0]] = 0
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_std[index_col[i][0]] = 0

        if (end_timestamp - begin_timestamp) > 48 * 3600:
            mn = TestDTW.Matrix_Completion_3(mn)
            # mn = Centralized_with_Outliers(mn)
            [a, b] = mn.shape

            result = TestDTW.Distance_Metric_Cos(mn, sensor_len)
            result = TestDTW.Dimension_Reduction_PCA(result)

            # result = Dimension_Reduction_MDS(feature_matrix)  # 降维
            '''
            聚类： 每类标不同颜色
            '''

            cluster = TestDTW.Cluster_DBSCAN(result)
            cluster_label = cluster.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)

            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all

            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster": cluster_label[i], "mean": col_mean[i],
                                                        "std": col_std[i], "nan": col_nan[i] / a,
                                                        "accuracy": mn_accuracy_count[i]}
            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type

            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],
                     "nan": col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency": col_inconsistency_all[i]})
            print(tree)
            return tree
        else:
            mn = mn.T

            mn = TestDTW.Matrix_Completion_2(mn)
            [a, b] = mn.shape
            dbscan = DBSCAN(eps=35,
                            min_samples=2,
                            metric=lambda a, b: DTW.distance(a, b))  # 可以自定义距离函数
            cluster_label = dbscan.fit_predict(mn)
            # print(cluster_label)

            cluster_label = cluster_label.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)

            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all

            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster": cluster_label[i], "mean": col_mean[i],

                                                        "std": col_std[i], "nan": col_nan[i] / a,
                                                        "accuracy": mn_accuracy_count[i]}

            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type

            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],
                     "nan": col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency":col_inconsistency_all[i]})
            print(tree)
            return tree

    @staticmethod
    def mobile_cluster(begintime, endtime):
        begin_date = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
        begin_timestamp = time.mktime(begin_date.timetuple())
        end_timestamp = time.mktime(end_date.timetuple())
        cursor = connection.cursor()
        inconsistency_data = [
            11.81,
            12.51,
            6.70,
            0.85,
            0.80,
            6.90,
            2.68,
            3.90,
            3.77,
            1.65,
            4.20,
            3.93,
            2.02,
            1.52,
            0.54,
            1.67,
            19.05,
            22.52,
            8.18,
            27.36,
            19.71,
            5.03,
            1.21,
            9.07,
            13.21,
            18.61,
            10.16,
            0.53,
            0.72,
            1.21,
            0.96,
            15.27,
            14.93,
            16.20,
            16.31,
            26.59,
            6.37,
            27.33,
            26.84,
            18.59,
            16.48,
            20.10,
            18.50,
            27.22,
            24.62,
            25.92,
            24.46,
            27.05,
            27.18,
            20.80
        ]

        if (end_timestamp - begin_timestamp) > 6 * 3600:
            # elif ((end_timestamp - begin_timestamp)) > 3 * 3600 and (end_timestamp - begin_timestamp) <= 48 * 3600:
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00'), sid, avg(value), AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from mobilesensorreadings where timestamp between '{}' and '{}' GROUP BY concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'), sid)".format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            mobile_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                mobile_sensors.add(i[1])
            mobile_sensors = list(mobile_sensors)
            begin = datetime.datetime.strptime(begintime, '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs1 = {}
            mobile_sensors_all = []
            for i in range(1, 51):
                mobile_sensors_all.append(i)

            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs1[date_str] = {}
                for i in mobile_sensors:
                    obs1[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs1[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(begintime[0:14] + "00", '%Y-%m-%d %H:%M').timetuple())
            obs1_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M')
                obs1_accuracy[date_str] = {}
                for i in mobile_sensors:
                    obs1_accuracy[date_str][i] = math.nan
                current += 3600
            for d in data:
                obs1_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs1_accuracy)
            for value in obs1_accuracy.values():
                tmp.append(list(value.values()))
            m_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                m_accuracy = np.vstack((m_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs1)
            for value in obs1.values():
                tmp.append(list(value.values()))
            m = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                m = np.vstack((m, t))  # 120 * 50
            print(m.shape)
            print(m_accuracy.shape)
        else:
            cursor.execute(
                '''select DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE), sid, avg(value), AVG(LENGTH(SUBSTR(CAST(`value` AS CHAR),LOCATE('.',`value`)+1))) from mobilesensorreadings where timestamp between '{}' and '{}' GROUP BY DATE_ADD(CONCAT(DATE_FORMAT(timestamp,'%Y-%m-%d %H:'),FLOOR(MINUTE(timestamp)/10),"0"),INTERVAL 10 MINUTE),sid'''.format(
                    begintime, endtime))
            alldata = cursor.fetchall()
            data = []
            mobile_sensors = set()
            for i in alldata:
                data.append({'time': i[0], 'sid': i[1], 'value': i[2], 'accuracy': round(i[3])})
                mobile_sensors.add(i[1])
            mobile_sensors_all = []

            for i in range(1, 51):
                mobile_sensors_all.append(i)
            mobile_sensors = list(mobile_sensors)
            begin = datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S')
            end = datetime.datetime.strptime(alldata[-1][0], '%Y-%m-%d %H:%M:%S')
            begin_timestamp = time.mktime(begin.timetuple())
            end_timestamp = time.mktime((end.timetuple()))
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs1 = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs1[date_str] = {}
                for i in mobile_sensors:
                    obs1[date_str][i] = math.nan
                current += 600
            for d in data:
                obs1[d['time']][d['sid']] = d['value']

            '''
                精度计算：按照timerang内每个sid的精度个数衡量
            '''
            current = time.mktime(datetime.datetime.strptime(alldata[0][0], '%Y-%m-%d %H:%M:%S').timetuple())
            obs1_accuracy = {}
            while current <= end_timestamp:
                date_str = datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S')
                obs1_accuracy[date_str] = {}
                for i in mobile_sensors:
                    obs1_accuracy[date_str][i] = math.nan
                current += 600
            for d in data:
                obs1_accuracy[d['time']][d['sid']] = d['accuracy']

            tmp = []
            obs_accuracy_len = len(obs1_accuracy)
            for value in obs1_accuracy.values():
                tmp.append(list(value.values()))
            m_accuracy = np.array(tmp[0])
            for i in range(1, obs_accuracy_len):
                t = np.array(tmp[i])
                m_accuracy = np.vstack((m_accuracy, t))  # 120 * 50

            tmp = []
            obs_len = len(obs1)
            for value in obs1.values():
                tmp.append(list(value.values()))
            m = np.array(tmp[0])
            for i in range(1, obs_len):
                t = np.array(tmp[i])
                m = np.vstack((m, t))  # 120 * 50
            print(m.shape)
            print(m_accuracy.shape)

        sensor_length_all = 50
        sensors_title_all = [('m' + str(i)) for i in mobile_sensors_all]
        sensors_title = [('m' + str(i)) for i in mobile_sensors]
        sensor_len = len(sensors_title)
        mn = m
        mn_accuracy = m_accuracy
        # print(mn)
        '''
        不确定性指标计算
        '''
        index_nan_mn = np.argwhere(np.isnan(mn))
        nan_col = index_nan_mn[:, 1]
        uniques = np.unique(nan_col)
        nan_result = []
        for i in set(nan_col):
            nan_result.append(nan_col.tolist().count(i))
        # print(nan_result)
        # print(len(nan_result))
        # print(len(uniques))
        col_nan = np.zeros(sensor_len)
        for i in range(len(col_nan)):
            for j in range(len(uniques)):
                col_nan[uniques[j]] = nan_result[j]

        # mn_accuracy = TestDTW.Matrix_Completion_4(mn_accuracy)
        [a, b] = mn_accuracy.shape
        print(a, b)
        mn_accuracy_count = np.nanmean(mn_accuracy, axis=0)
        mn_accuracy_count = np.around(mn_accuracy_count).tolist()
        print(mn_accuracy_count)
        # mn_accuracy_count = []
        # [a, b] = mn_accuracy.shape
        # for i in range(b):
        #     tmp = np.unique(mn_accuracy[:, i])
        #     print(tmp)
        #     mn_accuracy_count.append(len(tmp))
        # print(mn_accuracy_count)
        # print(len(mn_accuracy_count))

        col_mean = np.nanmean(mn, axis=0).tolist()  # 均值
        col_std = np.nanstd(mn, axis=0).tolist()  # 标准差
        index_col = np.argwhere(np.isnan(col_mean))
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_mean[index_col[i][0]] = 0
        if len(index_col) > 0:
            for i in range(len(index_col)):
                col_std[index_col[i][0]] = 0

        # 不一致性衡量
        col_inconsistency = {}
        for i in range(len(inconsistency_data)):
            if i + 1 in mobile_sensors:
                col_inconsistency[i + 1] = inconsistency_data[i]
        col_inconsistency = list(col_inconsistency.values())
        col_inconsistency = col_inconsistency
        print(col_inconsistency)

        if (end_timestamp - begin_timestamp) > 48 * 3600:
            mn = TestDTW.Matrix_Completion_3(mn)
            # mn = Centralized_with_Outliers(mn)
            [a, b] = mn.shape

            result = TestDTW.Distance_Metric_Cos(mn, sensor_len)
            result = TestDTW.Dimension_Reduction_PCA(result)

            # result = Dimension_Reduction_MDS(feature_matrix)  # 降维
            '''
            聚类： 每类标不同颜色
            '''

            cluster = TestDTW.Cluster_DBSCAN(result)
            cluster_label = cluster.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)

            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all

            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster": cluster_label[i], "mean": col_mean[i],
                                                        "std": col_std[i], "nan": col_nan[i] / a,
                                                        "accuracy": mn_accuracy_count[i],
                                                        "inconsistency": col_inconsistency[i]}
            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
                    col_inconsistency_all[i] = have_value_sensors[sensors_title_all[i]]["inconsistency"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type

            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],
                     "nan": col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency": col_inconsistency_all[i]})
            print(tree)
            return tree
        else:
            mn = mn.T
            mn = TestDTW.Matrix_Completion_2(mn)
            [a, b] = mn.shape
            dbscan = DBSCAN(eps=35,
                            min_samples=2,
                            metric=lambda a, b: DTW.distance(a, b))  # 可以自定义距离函数
            cluster_label = dbscan.fit_predict(mn)
            # print(cluster_label)

            cluster_label = cluster_label.tolist()
            class_type = list(set(cluster_label))
            class_type.sort(key=cluster_label.index)

            cluster_label_all = [-2] * sensor_length_all
            col_nan_all = [1] * sensor_length_all
            col_std_all = [0] * sensor_length_all
            col_mean_all = [1] * sensor_length_all
            col_accuracy = [0] * sensor_length_all
            col_inconsistency_all = [-5] * sensor_length_all

            have_value_sensors = {}
            for i in range(sensor_len):
                have_value_sensors[sensors_title[i]] = {"cluster": cluster_label[i], "mean": col_mean[i],
                                                        "std": col_std[i], "nan": col_nan[i] / a,
                                                        "accuracy": mn_accuracy_count[i],
                                                        "inconsistency": col_inconsistency[i]}
            # print(have_value_sensors)

            for i in range(sensor_length_all):
                if have_value_sensors.__contains__(sensors_title_all[i]):
                    cluster_label_all[i] = have_value_sensors[sensors_title_all[i]]["cluster"]
                    col_nan_all[i] = have_value_sensors[sensors_title_all[i]]["nan"]
                    col_std_all[i] = have_value_sensors[sensors_title_all[i]]["std"]
                    col_mean_all[i] = have_value_sensors[sensors_title_all[i]]["mean"]
                    col_accuracy[i] = have_value_sensors[sensors_title_all[i]]["accuracy"]
                    col_inconsistency_all[i] = have_value_sensors[sensors_title_all[i]]["inconsistency"]
            if -2 in cluster_label_all:
                class_type = [-2] + class_type

            tree = {"name": "cluster", "children": []}
            for i in range(len(class_type)):
                tree["children"].append({"name": class_type[i], "children": []})
            for i in range(len(cluster_label_all)):
                for j in range(len(tree["children"])):
                    if tree["children"][j]["name"] == cluster_label_all[i]:
                        tmp = j
                tree["children"][tmp]["children"].append(
                    {"name": sensors_title_all[i], "mean": col_mean_all[i], "std": col_std_all[i],
                     "nan": col_nan_all[i], "accuracy": col_accuracy[i], "inconsistency": col_inconsistency_all[i]})
            print(tree)
            return tree



if __name__ == "__main__":
    # TestDTW.test_cluster_effect_agg()
    tree = TestDTW.static_mobile_cluster('2020-04-06 00:00:00', '2020-04-06 22:00:00')
    # tree = TestDTW.static_cluster('2020-04-06 06:34:02', '2020-04-09 22:12:12')
    # tree = TestDTW.mobile_cluster('2020-04-06 04:10:10', '2020-04-10 10:00:10')