from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import paymentAccount
from django.contrib import messages
# Create your views here.
def changeCartNumber(request):
    if request.method == 'POST':
        cartNumber = request.POST.get('cardNumber')
        name = request.POST.get('name')
        user=User.objects.get(is_superuser=True)

        payment=paymentAccount.objects.get(user=user)
        payment.number=cartNumber
        payment.nameCart=name
        payment.save()
        messages.success(request, 'تغییر شماره کارت با موفقیت انجام شد')
        response={
            'messages': 'تغییر شماره کارت با موفقیت انجام شد'
        }
        return JsonResponse(response)
    else:
        messages.success(request, 'تغییر شماره کارت با مشکل مواجه شد')
        return JsonResponse({'status': True})