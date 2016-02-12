from django.shortcuts import render
from datetime import datetime
from ubike.models import station
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import gzip
import json


def ubike(request):
	url = urllib.request.Request("http://data.taipei/youbike")
	url.add_header("Accept-encoding", "gzip")
	try :
		response = urllib.request.urlopen(url)
	except urllib.HTTPError as e:
		print(e)
	except urllib.URLError as e:
		print(e)
	else:
	    data =json.loads(gzip.open(response,'r').read().decode("utf8"))
	    if not station.objects.all():
	    	station_create(data)
	    else:
	    	station_update(data)
	return render(request,'ubike.html',{
		'refresh_time': datetime.now(),
		'station_data': data,
		})

def station_create(new_data):
	all_stations = new_data["retVal"]
	for s,v in all_stations.items():
		station.objects.create(
			id = v["sno"],
			sno = v["sno"],
			sna = v["sna"],
			tot = v["tot"],
			sbi = int(v["sbi"]),
			sarea = v["sarea"],
			mday = datetime.strptime(v["mday"],"%Y%m%d%H%M%S"),
			lat = float(v["lat"]),
			lng = float(v["lng"]),
			ar = v["ar"],
			sareaen = v["sareaen"],
			aren = v["aren"],
			bemp = int(v["bemp"]),
			act = v["act"]
			)

def station_update(new_data):
	all_stations = new_data["retVal"]
	for s,v in all_stations.items():
		theStation = station.objects.filter(id = s)
		theStation.update(
			tot = v["tot"],
			sbi = int(v["sbi"]),
			mday = datetime.strptime(v["mday"],"%Y%m%d%H%M%S"),
			bemp = int(v["bemp"]),
			act = v["act"]
			)



