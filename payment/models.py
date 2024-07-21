from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jalali_models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class paymentAccount(models.Model):
    number = models.CharField(max_length=16,null=True)
    nameCart=models.CharField(max_length=100,null=True,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moneyInventory=models.DecimalField(max_digits=12, decimal_places=0,default=0)
    goldInventory=models.DecimalField(max_digits=12, decimal_places=6,default=0)
    #endurance=models.DecimalField(max_digits=12, decimal_places=0,default=0)
class paymentDate(models.Model):
    pass
class Invoice(models.Model):
    date=jalali_models.jDateField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(2)])

class sellRequst(Invoice):
    image=models.ImageField(upload_to="media/sell/")
    def __str__(self):
        return 'واریز'
class BuyRequst(Invoice):
    number = models.CharField(max_length=16)
    nameCart = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return 'برداشت'
class convertGoldRequst(Invoice):
    gold=models.DecimalField(max_digits=6, decimal_places=6)
    def __str__(self):
        return 'تبدیل'