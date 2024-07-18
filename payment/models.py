from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jalali_models

# Create your models here.
class paymentAccount(models.Model):
    number = models.CharField(max_length=16, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moneyInventory=models.DecimalField(max_digits=12, decimal_places=0,default=0)
    goldInventory=models.DecimalField(max_digits=12, decimal_places=6,default=0)
    #endurance=models.DecimalField(max_digits=12, decimal_places=0,default=0)
    def __str__(self):
        return f'{str(self.number) + self.user.last_name}'
class Invoice(models.Model):
    date=jalali_models.jDateField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

class sellRequst(Invoice):
    image=models.ImageField(upload_to="media/sell/")
class BuyRequst(Invoice):
    number = models.CharField(max_length=16)
class convertGoldRequst(Invoice):
    gold=models.DecimalField(max_digits=6, decimal_places=6)