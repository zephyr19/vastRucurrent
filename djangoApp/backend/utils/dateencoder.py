import json  
import datetime  

"""
使用python自带的json，将数据转换为json数据时，datetime格式的数据报错：django Object of type 'datetime' is not JSON serializable。此时重写构造json类，遇到日期特殊处理，其余的用内置的就行。
"""
class DateEncoder(json.JSONEncoder):  
	def default(self, obj):  
		if isinstance(obj, datetime.datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')  
		elif isinstance(obj, date):
			return obj.strftime("%Y-%m-%d")  
		else:  
			return json.JSONEncoder.default(self, obj) 