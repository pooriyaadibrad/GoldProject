from django.contrib import admin
from . import models

# Register your models here.
"""
class sell(admin.TabularInline):
    model = models.sellRequst

class Gold(admin.TabularInline):
    model = models.convertGoldRequst
class Buy(admin.TabularInline):
    model = models.BuyRequst


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {'fields': []},
        ),
    ]
    inlines = [Buy,sell,Gold]


@admin.register(models.BuyRequst)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [sell, Gold]
"""
class BuyRequstAdmin(admin.ModelAdmin):
    list_display = ['price','date','user']

admin.site.register(models.BuyRequst, BuyRequstAdmin)
admin.site.register(models.convertGoldRequst)
admin.site.register(models.sellRequst)
admin.site.register(models.paymentAccount)
admin.site.register(models.GetGoldRequst)
admin.site.register(models.ConvertMoneyRequst)
class paymentDateAdmin(admin.ModelAdmin):
    list_display = [ 'price','datetime']
admin.site.register(models.paymentDate, paymentDateAdmin)