from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import paymentAccount,BuyRequst,sellRequst,convertGoldRequst
from django.contrib import messages
from account.models import person
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
        requestType=request.POST['comboBox']
        startDate=request.POST['start']
        endDate=request.POST['end']
        if startDate!='' and endDate!='':
            start = startDate.replace('/', '-')
            end = endDate.replace('/', '-')
            if requestType == 'واریز وجه':
                sell = sellRequst.objects.filter(date__range=(start, end))
                sell1 = []
                sell1.extend(sell)
                for b in sell1:
                    user1 = person.objects.filter(user=b.user).first()
                    payment1 = paymentAccount.objects.filter(user=b.user).first()
                    sell1[sell1.index(b)] = [b, user1,payment1]
                return render(request,template_name='Report.html',context={'data':sell1})

            elif requestType == 'برداشت وجه':
                Buy = BuyRequst.objects.filter(date__range=(start, end))
                Buy1=[]
                Buy1.extend(Buy)
                for b in Buy1:
                    user1=person.objects.filter(user=b.user).first()
                    payment1 = paymentAccount.objects.filter(user=b.user).first()
                    if payment1 is not None:
                        Buy1[Buy1.index(b)] = [b,user1,payment1]
                    else:
                        Buy1[Buy1.index(b)] = [b, user1, payment1]

                return render(request, template_name='Report.html', context={'data': Buy1})

            else:
                Gold = convertGoldRequst.objects.filter(date__range=(start, end))
                Gold1 = []
                Gold1.extend(Gold)
                for b in Gold1:
                    user1 = person.objects.filter(user=b.user).first()
                    payment1 = paymentAccount.objects.filter(user=b.user).first()
                    Gold1[Gold1.index(b)] = [b, user1,payment1]
                return render(request,template_name='Report.html',context={'data':Gold1})
        else:
            messages.success(request,'لطفا فیلد ها زمانی را پر کنید')
            return redirect('report')
    else:
        messages.success(request,'درخواست به درستی انجام نشد')
        redirect('report')




"""
def getReport(request):
    if request.method == 'POST':
        start=str(request.POST.get('start'))
        end=str(request.POST.get('end'))
        requestType=request.POST.get('requestType')
        start=start.replace('/','-')
        end=end.replace('/','-')
        if requestType=='واریز وجه':
            sell=sellRequst.objects.filter(date__range=(start,end))
            return JsonResponse({'status': True})

        elif requestType=='برداشت وجه':
            Buy = BuyRequst.objects.filter(date__range=(start, end))
            return JsonResponse({'status': True,'Gold':Buy})
        else:
            Gold = convertGoldRequst.objects.filter(date__range=(start, end))
            return JsonResponse({'status': True,'Gold':Gold})
    else:
        return JsonResponse({'status': False})
"""