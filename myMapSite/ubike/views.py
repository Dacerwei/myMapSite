from django.shortcuts import render
from datetime import datetime

def ubike(request):
	return render(request,'ubike.html',{
		'refresh_time': datetime.now(),
		})