import sys
import os
import django
import json
from django.db import connection

# 找到项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RadiationVis.settings')
django.setup()

from backend import models

def query1():
	# 使用raw查询
	all = models.StaticSensorLocations.objects.raw("select * from staticsensorlocations")
	tmp = [str(o) for o in list(all)]
	print(json.dumps({'data': tmp}))

def query2():
	# 使用Connection、Cursor查询
	cursor = connection.cursor()
	# Data retrieval operation - no commit required
	cursor.execute("select * from staticsensorlocations")
	desc = cursor.description
	data = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
	print(data)

if __name__ == "__main__":
	query2()

	