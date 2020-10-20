from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from backend.models import StaticSensorLocations, StaticSensorReadings, MobileSensorReadings
from backend.dataprocessing.cluster_dtw import TestDTW
import json
import time
import datetime

# Create your views here.


def testdb(request):
    all = StaticSensorLocations.objects.all().values()
    return HttpResponse(json.dumps({'data': list(all)}), content_type='application/json')


@csrf_exempt
def findSrBySid(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        # 首先检查是静态传感器还是动态传感器
        category = params['category']
        if category == 'mobile':
            responseData = MobileSensorReadings.objects.filter(
                sid=params['sid']).values()
        elif category == 'static':
            responseData = StaticSensorReadings.objects.filter(
                sid=params['sid']).values()
        return HttpResponse(json.dumps(list(responseData), cls=DateEncoder), content_type='application/json')


@csrf_exempt
def calSensorClusters(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        data = TestDTW.static_mobile_cluster(
            params['begintime'], params['endtime'])
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def calTimeSeries(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        begintime_str = params['begintime']
        endtime_str = params['endtime']
        begin_date = datetime.datetime.strptime(
            begintime_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')
        begin_timestamp = time.mktime(begin_date.timetuple())
        end_timestamp = time.mktime(end_date.timetuple())

        static_data = None
        mobile_data = None
        cursor = connection.cursor()

        # 如果时间间隔超过6小时，按小时聚合，否则按分钟聚合
        if (end_timestamp - begin_timestamp) > 6 * 3600:
            # 查询动态数据
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00:00') as time, avg(value) as avg, std(value) as std, std(value)/sqrt(count(*)) as standarderror from mobilesensorreadings where timestamp >= '{0}' and timestamp < '{1}' and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H')".format(begintime_str, endtime_str))

            desc = cursor.description
            alldata = cursor.fetchall()
            mobile_data = [dict(zip([col[0] for col in desc], row))
                           for row in alldata]

            # 查询静态数据
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00:00') as time, avg(value) as avg, std(value) as std, std(value)/sqrt(count(*)) as standarderror from staticsensorreadings where timestamp >= '{0}' and timestamp < '{1}' and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H')".format(begintime_str, endtime_str))

            desc = cursor.description
            alldata = cursor.fetchall()
            static_data = [dict(zip([col[0] for col in desc], row))
                           for row in alldata]
        else:
            # 查询动态数据
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i'),':00') as time, avg(value) as avg, std(value) as std, std(value)/sqrt(count(*)) as standarderror from mobilesensorreadings where timestamp >= '{0}' and timestamp < '{1}' and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i')".format(begintime_str, endtime_str))
            desc = cursor.description
            alldata = cursor.fetchall()
            mobile_data = [dict(zip([col[0] for col in desc], row))
                           for row in alldata]

            # 查询静态数据
            cursor.execute(
                "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i'),':00') as time, avg(value) as avg, std(value) as std, std(value)/sqrt(count(*)) as standarderror from staticsensorreadings where timestamp >= '{0}' and timestamp < '{1}' and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i')".format(begintime_str, endtime_str))
            desc = cursor.description
            alldata = cursor.fetchall()
            static_data = [dict(zip([col[0] for col in desc], row))
                           for row in alldata]

        data = {'mobile': mobile_data, 'static': static_data}

        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def calTimeSeriesBySid(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        category = params['category']
        sid = params['sid']
        begintime_str = params['begintime']
        endtime_str = params['endtime']
        begin_date = datetime.datetime.strptime(
            begintime_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')
        begin_timestamp = time.mktime(begin_date.timetuple())
        end_timestamp = time.mktime(end_date.timetuple())

        data = None
        cursor = connection.cursor()

        # 如果时间间隔超过三小时，按小时聚合，否则按分钟聚合
        if (end_timestamp - begin_timestamp) > 6 * 3600:
            if category == 'mobile':
                # 查询动态数据
                cursor.execute(
                    "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00:00') as time, avg(value) as avg, std(value)/sqrt(count(*)) as standarderror, std(value) as std from mobilesensorreadings where timestamp >= '{0}' and timestamp < '{1}' and sid = {2} and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H')".format(begintime_str, endtime_str, sid))

                desc = cursor.description
                alldata = cursor.fetchall()
                data = [dict(zip([col[0] for col in desc], row))
                        for row in alldata]

            else:

                # 查询静态数据
                cursor.execute(
                    "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H'),':00:00') as time, avg(value) as avg, std(value)/sqrt(count(*)) as standarderror, std(value) as std from staticsensorreadings where timestamp >= '{0}' and timestamp < '{1}' and sid = {2} and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H')".format(begintime_str, endtime_str, sid))

                desc = cursor.description
                alldata = cursor.fetchall()
                data = [dict(zip([col[0] for col in desc], row))
                        for row in alldata]

        else:
            if category == 'mobile':
                # 查询动态数据
                cursor.execute(
                    "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i'),':00') as time, avg(value) as avg, std(value)/sqrt(count(*)) as standarderror, std(value) as std from mobilesensorreadings where timestamp >= '{0}' and timestamp < '{1}' and sid = {2} and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i')".format(begintime_str, endtime_str, sid))
                desc = cursor.description
                alldata = cursor.fetchall()
                data = [dict(zip([col[0] for col in desc], row))
                        for row in alldata]

            else:
                # 查询静态数据
                cursor.execute(
                    "select concat(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i'),':00') as time, avg(value) as avg, std(value)/sqrt(count(*)) as standarderror, std(value) as std from staticsensorreadings where timestamp >= '{0}' and timestamp < '{1}' and sid = {2} and value < 15000 group by DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i')".format(begintime_str, endtime_str, sid))
                desc = cursor.description
                alldata = cursor.fetchall()
                data = [dict(zip([col[0] for col in desc], row))
                        for row in alldata]

        return HttpResponse(json.dumps(data), content_type='application/json')
