from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from ubike.models import station
from ubike.models import lasted_station
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import gzip
import json
from .forms import dateSearch

def youbike(request):
	allStations = []
	search_date_from = ""
	search_date_to = ""
	dateForm = dateSearch(request.GET)

	if dateForm.is_valid():
		print("valid succeed")
		print("search data from dates: "+dateForm.cleaned_data['from_date'].__str__()+" to "+dateForm.cleaned_data['to_date'].__str__())
		search_date_from = dateForm.cleaned_data['from_date']
		search_date_to = dateForm.cleaned_data['to_date']

		for x in range(1,20):
			temp = station.objects.filter(sno=x,datetime__gte = search_date_from,datetime__lte = search_date_to)
			if(temp):
				aStation = {"sno":x,
							"ar":temp[0].ar,
							"position":[temp[0].lat,temp[0].lng]}

				station_data = []

				for d in temp:
					station_data.append([d.datetime.strftime("%b/%d %H:%M"),d.sbi,d.bemp])

				aStation.update({"data":station_data})
				allStations.append(aStation)
	else:
		print("valid failed")

	return render(request,'youbike.html',{
		'date_from_default':str(search_date_from),
		'date_to_default':str(search_date_to),
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



