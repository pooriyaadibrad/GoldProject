from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import paymentAccount,BuyRequst,sellRequst,convertGoldRequst
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
def checkOrder(request):
    if request.method == 'POST':
        choice=request.POST.get('choice')
        requestid=request.POST.get('request')
        requestName=request.POST.get('requestName')
        if choice=='1':
          if requestName=='برداشت':
              buy=BuyRequst.objects.get(id=requestid)
              buy.status=2
              buy.save()
              return JsonResponse({'status': True})
          elif requestName=='واریز':
              sell = sellRequst.objects.get(id=requestid)
              sell.status = 2
              sell.save()
              return JsonResponse({'status': True})
          else:
              Gold = convertGoldRequst.objects.get(id=requestid)
              Gold.status = 2
              Gold.save()
              return JsonResponse({'status': True})
        else:
            if requestName == 'برداشت':
                buy = BuyRequst.objects.get(id=requestid)
                buy.status = 1
                buy.save()
                return JsonResponse({'status': True})
            elif requestName == 'واریز':
                sell = sellRequst.objects.get(id=requestid)
                sell.status = 1
                sell.save()
                return JsonResponse({'status': True})
            else:
                Gold = convertGoldRequst.objects.get(id=requestid)
                Gold.status = 1
                Gold.save()
                return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})
def getReport(request):
    if request.method == 'POST':
        start=str(request.POST.get('start'))
        end=str(request.POST.get('end'))
        requestType=request.POST.get('requestType')
        start=start.replace('/','-')
        end=end.replace('/','-')
        if requestType=='واریز وجه':
            sell=sellRequst.objects.filter(date__range=(start,end))
            return JsonResponse({'status': True,'Gold':sell})

        elif requestType=='برداشت وجه':
            Buy = BuyRequst.objects.filter(date__range=(start, end))
            return JsonResponse({'status': True,'Gold':Buy})
        else:
            Gold = convertGoldRequst.objects.filter(date__range=(start, end))
            return JsonResponse({'status': True,'Gold':Gold})
    else:
        return JsonResponse({'status': False})
