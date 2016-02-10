from django.shortcuts import render
from datetime import datetime
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
	    data =gzip.open(response,'r').read().decode("utf8")
	    dataInJson = json.loads(data)
	return render(request,'ubike.html',{
		'refresh_time': datetime.now(),
		'station_data': dataInJson,
		})