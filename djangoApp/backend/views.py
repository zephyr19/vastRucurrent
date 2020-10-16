from django.shortcuts import render
from django.http import HttpResponse
from backend.models import StaticSensorLocations, StaticSensorReadings, MobileSensorReadings
import json

# Create your views here.


def testdb(request):
    all = StaticSensorLocations.objects.all().values()
    return HttpResponse(json.dumps({'data': list(all)}), content_type='application/json')
