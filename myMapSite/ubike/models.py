from django.db import models

class station(models.Model):
	sno = models.CharField(max_length=100)
	sna = models.CharField(max_length=100)
	tot = models.IntegerField()
	sbi = models.IntegerField()
	sarea = models.CharField(max_length=100)
	mday = models.DateTimeField()
	lat = models.FloatField()
	lng = models.FloatField()
	ar = models.CharField(max_length=100)
	sareaen = models.CharField(max_length=100)
	aren = models.CharField(max_length=100)
	bemp = models.IntegerField()
	act = models.BooleanField(default=True)

	def __str__(self):
		return self.sna