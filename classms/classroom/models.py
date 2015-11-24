from django.db import models

# Create your models here.
class user(models.Model):
	username=models.CharField(max_length=10)
	email=models.EmailField(primary_key=True)
	comNum=models.IntegerField()
	curRoomNum=models.IntegerField()
	hisRoomNum=models.IntegerField()
	def __unicode__(self):
         return self.username

class room(models.Model):
	location=models.CharField(max_length=20)
	floor=models.IntegerField()
	number=models.IntegerField()
	isUsed=models.BooleanField()
	isOrder=models.BooleanField()
	lockBy=models.ForeignKey(user)
	def __unicode__(self):
         return self.location+self.number

class comment(models.Model):
	room=models.ForeignKey(room)
	user=models.ForeignKey(user)
	comment=models.CharField(max_length=200)
	time=models.DateTimeField(auto_now=True)
	def __unicode__(self):
         return self.comment
