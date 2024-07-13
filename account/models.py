from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class user(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    Mobile = models.CharField(max_length=15,default='09')
    address = models.CharField(max_length =100,default='iran')
    LandlineNumber = models.CharField(max_length =50,default='011')
