from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jalali_models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class paymentAccount(models.Model):
    number = models.CharField(max_length=16, null=True, blank=True)
    sheba = models.CharField(max_length=26, null=True, blank=True)
    nameCart = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moneyInventory = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    goldInventory = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    # endurance=models.DecimalField(max_digits=12, decimal_places=0,default=0)
    def __str__(self):
        return f'{self.user.username} - {self.user.first_name} - {self.user.last_name}'


class paymentDate(models.Model):
    price = models.CharField(max_length=50, null=True)
    datetime = jalali_models.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.datetime} {self.price}'


class Invoice(models.Model):
    date = jalali_models.jDateField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])


class sellRequst(Invoice):
    image = models.ImageField(upload_to="sell/")

    def __str__(self):
        return 'واریز'


class BuyRequst(Invoice):
    def __str__(self):
        return 'برداشت'


class convertGoldRequst(Invoice):
    gold = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return 'تبدیل'


class ConvertMoneyRequst(Invoice):
    gold = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return 'تبدیل به پول'


class GetGoldRequst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])
    date = jalali_models.jDateField(auto_now_add=True)
    gold = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return 'دریافت طلا'
