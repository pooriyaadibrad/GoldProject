from django.contrib import admin
from . import models
# Register your models here.
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
"""

@admin.register(models.BuyRequst)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [sell, Gold]
"""


admin.site.register(models.paymentAccount)
