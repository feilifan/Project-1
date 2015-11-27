from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class People(models.Model):
    user = models.ForeignKey(User,related_name="user_people")
    email = models.EmailField()
    nickname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    school_number = models.CharField(max_length=15)
    def _unicode_(self):
        return self.name
class Classroom(models.Model):
    hoster = models.ForeignKey(People,related_name="hoster_room")
    name = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    size = models.CharField(max_length=30)#10-30 30-50 50-100 100-200 200+
    multimedia = models.BooleanField(default=True)    
    time_access = models.CharField(max_length=50)
    def _unicode_(self):
        return self.name
        
class Apply_list(models.Model):
    applyer = models.ForeignKey(People,related_name="applyer_list")
    time = models.CharField(max_length=30)            #YYYY-MM-DD-HH:MM-HH:MM
    hostname = models.CharField(max_length=30)
    room = models.CharField(max_length=30)            
    state = models.CharField(max_length=30)           
    pasttime = models.BooleanField(default=False)
    reason = models.CharField(max_length=100)
    def _unicode_(self):
        return self.name
        
class Discuss_list(models.Model):
    room = models.CharField(max_length=30)
    discusser = models.ForeignKey(People,related_name="discusser_list")
    point = models.CharField(max_length=30)
    content = models.CharField(max_length=100)
    def _unicode_(self):
        return self.name