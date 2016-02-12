from django.db import models

class station(models.Model):
	sno = models.IntegerField(max_length=100)	#站點代號
	sna = models.CharField(max_length=100)	#場站名稱(中文)
	tot = models.IntegerField()	#場站總停車格
	sbi = models.IntegerField()	#場站目前車輛數量
	sarea = models.CharField(max_length=100)	#場站區域(中文)
	mday = models.DateTimeField()	#資料更新時間
	lat = models.FloatField()	#緯度
	lng = models.FloatField()	#經度
	ar = models.CharField(max_length=100)	#地址(中文)
	sareaen = models.CharField(max_length=100)	#場站區域(英文)
	aren = models.CharField(max_length=100)	#地址(英文)
	bemp = models.IntegerField()	#空位數量
	act = models.BooleanField(default=True)	#全站禁用狀態

	def __str__(self):
		return self.sna

