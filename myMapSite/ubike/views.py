from django.shortcuts import render
from django.utils import timezone
from datetime     import datetime
from ubike.models import station
from ubike.models import lasted_station
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import gzip
import json
from .forms import dateSearch
import os
from myMapSite.settings import BASE_DIR


def youbike(request):
	search_date_from = ""
	search_date_to = ""
	dateForm = dateSearch(request.GET)
	allStations = []
	if dateForm.is_valid():
		print("valid succeed")
		print("search data from dates: "+dateForm.cleaned_data['from_date'].__str__()+" to "+dateForm.cleaned_data['to_date'].__str__())
		search_date_from = dateForm.cleaned_data['from_date']
		search_date_to = dateForm.cleaned_data['to_date']

		#取得以站點id排序的原始資料
		allData = sorted(station.objects.filter(datetime__gte = search_date_from,datetime__lte = search_date_to),key = lambda x:x.sno)
		
		#紀錄目前站點id
		val = 0

		#暫時儲存目前處理的站點資料
		aStation = {}

		for i in allData:
			stationID = i.sno
			#此筆資料為一座新站點資料
			if(stationID != val):

				#若非第一筆資料則須先將暫存資料存入allStations
				if(len(allStations) > 0): 
					allStations.append(aStation)
				#建立新站點的暫存資料
				aStation = {
					'station_ID':stationID,
					'address':i.ar,
					'position':[i.lat,i.lng],
					'time_series_data':[[i.datetime.strftime("%b/%d %H:%M"),i.sbi,i.bemp]],
				}

				#將新建立的站點推入allStation
				allStations.append(aStation)

				#紀錄目前出裡的站點id
				val = stationID

			#此筆資料為一座舊站點資料
			elif (stationID == val):
				allStations[-1]['time_series_data'].append([i.datetime.strftime("%b/%d %H:%M"),i.sbi,i.bemp])

	else:
		print("valid failed")

	return render(request,'youbike.html',{
		'date_from_default':str(search_date_from),
		'date_to_default':str(search_date_to),
		'stations': allStations,
		'mrt_point':getGeoJsonFile("mrt_point.geojson"),
		'mrt_line':getGeoJsonFile("mrt_line.geojson"),
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

def getGeoJsonFile(filename):
	json_data = 'no data'
	file_path = os.path.join(BASE_DIR, "ubike/static/ubike/js/"+filename)
	with open(file_path) as json_file:
		print('json Open succeed')
		json_data = json.dumps(json_file.read())
	if len(json_data) > 0 :
		print('json load succeed')
		return json_data
	else:
		print('json load failed')
		return False

