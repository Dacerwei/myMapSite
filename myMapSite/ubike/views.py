from django.shortcuts import render
from datetime import datetime
from ubike.models import station
from django.utils import timezone
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import gzip
import json

def youbike(request):
	allStations = []
	for x in range(1,225):
		temp = station.objects.filter(sno=x,datetime__year=2016,datetime__month=2,datetime__day=28)
		if(temp):
			aStation = {"sno":x,"ar":temp[0].ar,"position":[temp[0].lat,temp[0].lng]}
			station_data = []
			for d in temp:
				station_data.append([d.datetime.strftime("%H:%M"),d.sbi,d.bemp])
			aStation.update({"data":station_data})
			allStations.append(aStation)

	return render(request,'youbike.html',{
		'stations': allStations,
		})


def youbikerealtime(request):
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
	    station_create(data) #將站點資料寫入資料庫
	    # if not station.objects.all():
	    # 	station_create(data)
	    # else:
	    # 	station_update(data)
	return render(request,'youbikerealtimemap.html',{
		'refresh_time': datetime.now(),
		'station_data': data,
		})

def station_create(new_data):
	all_stations = new_data["retVal"]
	for s,v in all_stations.items():
		station.objects.create(
			sno = int(v["sno"]),
			sna = v["sna"],
			snaen = v["snaen"],
			tot = v["tot"],
			sbi = int(v["sbi"]),
			sarea = v["sarea"],
			datetime = timezone.now(),
			#datetime = datetime.strptime(v["mday"],"%Y%m%d%H%M%S"),
			mday = v["mday"],
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



