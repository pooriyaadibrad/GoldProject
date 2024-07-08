from django.db import models

# Create your models here.

class user(models.Model):
    FullName = models.CharField(max_length =50)
    Mobile = models.CharField(max_length =15)
    NationCode = models.CharField(max_length =15)
    password = models.CharField(max_length =50,default=12345678)
    address = models.CharField(max_length =100,default='iran')
    LandlineNumber = models.CharField(max_length =50,default='011')
