from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import paymentAccount
from django.contrib import messages
# Create your views here.
def changeCartNumber(request):
    print('what conditions')
    if request.method == 'POST':
        cartNumber = request.POST.get('cardNumber')
        name = request.POST.get('name')
        user=User.objects.get(is_superuser=True)
        print(cartNumber)
        print(name)
        payment=paymentAccount.objects.get(user=user)
        payment.number=cartNumber
        payment.nameCart=name
        payment.save()
        messages.success(request, 'تغییر شماره کارت با موفقیت انجام شد')
        return redirect('changeCartNumber')
    else:
        messages.success(request, 'تغییر شماره کارت با مشکل مواجه شد')
        return redirect('changeCartNumber')