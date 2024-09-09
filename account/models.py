from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class person(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Mobile = models.CharField(max_length=15,default='09',blank=True)
    address = models.CharField(max_length =100,default='iran',blank=True)
    LandlineNumber = models.CharField(max_length =50,default='011',blank=True)
    blockStatus=models.BooleanField(default=True)
    picture = models.ImageField(upload_to="Nation_pictures/",default='default.jpg',blank=True)
    def __str__(self):
        return self.user.username