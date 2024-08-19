import jdatetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import paymentAccount, BuyRequst, sellRequst, convertGoldRequst
from django.contrib import messages
from account.models import person
from decimal import Decimal


# Create your views here.
def changeCartNumber(request):
    if request.method == 'POST':
        cartNumber = request.POST.get('cardNumber')
        name = request.POST.get('name')
        sheba = request.POST.get('sheba')
        user = User.objects.get(is_superuser=True)

        payment = paymentAccount.objects.get(user=user)
        payment.number = cartNumber
        payment.nameCart = name
        payment.sheba = sheba
        payment.save()
        messages.success(request, 'تغییر شماره کارت با موفقیت انجام شد')
        response = {
            'messages': 'تغییر شماره کارت با موفقیت انجام شد'
        }
        return JsonResponse(response)
    else:
        messages.success(request, 'تغییر شماره کارت با مشکل مواجه شد')
        return JsonResponse({'status': True})


def checkOrder(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        requestid = request.POST.get('request')
        requestName = request.POST.get('requestName')
        price = request.POST.get('price')
        if choice == '1':
            if requestName == 'برداشت':
                buy = BuyRequst.objects.get(id=requestid)
                account = paymentAccount.objects.get(user=buy.user)
                if account.moneyInventory >= int(price):
                    if account.nameCart == buy.user.first_name:
                        user = User.objects.get(is_superuser=True)
                        account1 = paymentAccount.objects.filter(user=user).first()
                        account.moneyInventory -= int(price)
                        account1.moneyInventory -= int(price)

                        account.save()
                        account1.save()
                        buy.status = 2
                        buy.save()
                        messages = 'برداشت انجام شد'
                        return JsonResponse({'status': True, 'messages': messages})
                    else:
                        messages = 'اسم دارنده کارت و اسم صاحب اکانت مطابق نیست'
                        return JsonResponse({'status': True, 'messages': messages})
                else:
                    messages = 'موجودی کاربر برای این درخواست کافی نیست'

                    return JsonResponse({'status': False, 'messages': messages})
            elif requestName == 'واریز':
                sell = sellRequst.objects.get(id=requestid)
                sell.status = 2
                account = paymentAccount.objects.get(user=sell.user)
                user = User.objects.get(is_superuser=True)
                account1 = paymentAccount.objects.filter(user=user).first()
                account.moneyInventory += int(price)
                account1.moneyInventory += int(price)

                account.save()
                account1.save()
                sell.save()
                messages = 'واریز انجام شد'
                return JsonResponse({'status': True, 'messages': messages})

            else:
                gold = request.POST.get('gold')

                Gold = convertGoldRequst.objects.get(id=requestid)
                Gold.status = 2
                account = paymentAccount.objects.get(user=Gold.user)
                if gold == '0.000000':
                    if account.moneyInventory >= int(price):
                        goldPrice = request.POST.get('goldPrice')
                        if goldPrice != None:
                            goldPrice = goldPrice.replace(',', '')
                            goldPrice = int(goldPrice)
                            user = User.objects.get(is_superuser=True)
                            account1 = paymentAccount.objects.filter(user=user).first()
                            account.moneyInventory -= int(price)
                            goldPrice /= 1000
                            account.goldInventory += Decimal(goldPrice)
                            account1.save()
                            account.save()
                            Gold.gold = goldPrice
                            Gold.save()
                            messages = 'تبدیل انجام شد'
                            return JsonResponse({'status': True, 'messages': messages})
                        else:
                            messages = 'فیلد مربوط به مقدار طلا یا مبلغ نباید خالی باشد'
                            return JsonResponse({'status': True, 'messages': messages})
                    else:

                        messages = 'موجودی کاربر برای این درخواست کافی نیست'

                        return JsonResponse({'status': False, 'messages': messages})
                else:
                    goldPrice = request.POST.get('goldPrice')
                    print(goldPrice, 'this for test')
                    print(type(goldPrice))
                    if goldPrice != '':
                        goldPrice = goldPrice.replace(',', '')

                        if account.moneyInventory >= int(goldPrice):
                            account.moneyInventory -= int(goldPrice)

                            account.goldInventory += Decimal(gold)
                            account.save()
                            Gold.price = goldPrice
                            Gold.save()
                            messages = 'تبدیل انجام شد'
                            return JsonResponse({'status': True, 'messages': messages})
                        else:

                            messages = 'موجودی کاربر برای این درخواست کافی نیست'

                            return JsonResponse({'status': False, 'messages': messages})
                    else:
                        messages = 'فیلد مربوط به مقدار طلا یا مبلغ نباید خالی باشد'
                        return JsonResponse({'status': True, 'messages': messages})


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
        requestType = request.POST['comboBox']
        startDate = request.POST['start']
        endDate = request.POST['end']
        if request.user.is_superuser:
            if startDate != '' and endDate != '':
                start = startDate.replace('/', '-')
                end = endDate.replace('/', '-')
                sell2 = sellRequst.objects.filter(date__range=(start, end)).all()
                buy2 = BuyRequst.objects.filter(date__range=(start, end)).all()
                gold2 = convertGoldRequst.objects.filter(date__range=(start, end)).all()
                resultSell = 0
                resultBuy = 0
                resultGold = 0
                for i, j, k in zip(sell2, buy2, gold2):
                    resultSell += i.price
                    resultBuy += j.price
                    resultGold += k.price
                if requestType == 'واریز وجه':
                    sell = sellRequst.objects.filter(date__range=(start, end)).all()
                    sell1 = []
                    sell1.extend(sell)
                    for b in sell1:
                        user1 = person.objects.filter(user=b.user).first()
                        payment1 = paymentAccount.objects.filter(user=b.user).first()
                        sell1[sell1.index(b)] = [b, user1, payment1, None]
                    return render(request, template_name='Report.html',
                                  context={'data': sell1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})

                elif requestType == 'برداشت وجه':
                    Buy = BuyRequst.objects.filter(date__range=(start, end)).all()
                    Buy1 = []
                    Buy1.extend(Buy)
                    for b in Buy1:
                        user1 = person.objects.filter(user=b.user).first()
                        payment1 = paymentAccount.objects.filter(user=b.user).first()

                        Buy1[Buy1.index(b)] = [b, user1, payment1, None]

                    return render(request, template_name='Report.html',
                                  context={'data': Buy1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})

                else:
                    Gold = convertGoldRequst.objects.filter(date__range=(start, end))
                    Gold1 = []
                    Gold1.extend(Gold)
                    for b in Gold1:
                        user1 = person.objects.filter(user=b.user).first()
                        payment1 = paymentAccount.objects.filter(user=b.user).first()
                        Gold1[Gold1.index(b)] = [b, user1, payment1, 'gold']
                    return render(request, template_name='Report.html',
                                  context={'data': Gold1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})
            else:
                messages.success(request, 'لطفا فیلد ها زمانی را پر کنید')
                return redirect('report')
        else:
            if startDate != '' and endDate != '':
                start = startDate.replace('/', '-')
                end = endDate.replace('/', '-')
                sell2 = sellRequst.objects.filter(date__range=(start, end)).all()
                buy2 = BuyRequst.objects.filter(date__range=(start, end)).all()
                gold2 = convertGoldRequst.objects.filter(date__range=(start, end)).all()
                resultSell = 0
                resultBuy = 0
                resultGold = 0
                for i, j, k in zip(sell2, buy2, gold2):
                    resultSell += i.price
                    resultBuy += j.price
                    resultGold += k.price
                if requestType == 'واریز وجه':
                    sell = sellRequst.objects.filter(date__range=(start, end)).filter(user=request.user).all()
                    sell1 = []
                    sell1.extend(sell)
                    for b in sell1:
                        user1 = person.objects.filter(user=request.user).first()
                        payment1 = paymentAccount.objects.filter(user=request.user).first()
                        sell1[sell1.index(b)] = [b, user1, payment1, None]
                    return render(request, template_name='ReportCustomer.html',
                                  context={'data': sell1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})

                elif requestType == 'برداشت وجه':
                    Buy = BuyRequst.objects.filter(date__range=(start, end)).filter(user=request.user).all()
                    Buy1 = []
                    Buy1.extend(Buy)
                    for b in Buy1:
                        user1 = person.objects.filter(user=request.user).first()
                        payment1 = paymentAccount.objects.filter(user=request.user).first()

                        Buy1[Buy1.index(b)] = [b, user1, payment1, None]

                    return render(request, template_name='ReportCustomer.html',
                                  context={'data': Buy1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})

                else:
                    Gold = convertGoldRequst.objects.filter(date__range=(start, end)).filter(user=request.user).all()
                    Gold1 = []
                    Gold1.extend(Gold)
                    for g in Gold1:
                        user1 = person.objects.filter(user=request.user)
                        payment1 = paymentAccount.objects.filter(user=request.user).first()
                        Gold1[Gold1.index(g)] = [g, user1, payment1, 'gold']
                    return render(request, template_name='ReportCustomer.html',
                                  context={'data': Gold1, 'resultSell': resultSell, 'resultBuy': resultBuy,
                                           'resultGold': resultGold})
            else:
                messages.success(request, 'لطفا فیلد ها زمانی را پر کنید')
                return redirect('reportCustomer')
    else:
        messages.success(request, 'درخواست به درستی انجام نشد')
        redirect('report')


def RegisterBuyRequest(request):
    if request.method == 'POST':
        invoice = request.FILES['files']
        price = request.POST['price']
        SellRequest = sellRequst(user=request.user, price=price, image=invoice, date=jdatetime.date.today())
        SellRequest.save()

        messages.success(request, 'بعد از بررسی مدیر نتیجه در همینجا ذخیره میشود')
        return redirect('settelmentCustomer')

    else:
        messages.success(request, 'در ثبت درخواست مشکلی پیش آمده است')
        return redirect('settelmentCustomer')


def DeleteTransaction(request, id, type):
    if type == 'واریز':
        sell = sellRequst.objects.get(id=id)
        sell.delete()
        messages.success(request, 'حذف موفقیت آمیز بود')
        return redirect('settelmentCustomer')
    elif type == 'برداشت':
        Buy = BuyRequst.objects.get(id=id)
        Buy.delete()
        messages.success(request, 'حذف موفقیت آمیز بود')
        return redirect('withdrawalCustomer')
    else:
        Gold = convertGoldRequst.objects.get(id=id)
        Gold.delete()
        messages.success(request, 'حذف موفقیت آمیز بود')
        return redirect('ChangeGoldCustomer')


def withdrawalCustomer(request):
    if request.method == 'POST':
        price = request.POST['price']
        paymentAccount1 = paymentAccount.objects.filter(user=request.user).first()
        if paymentAccount1.nameCart == request.user.first_name:
            Buy = BuyRequst(price=price, date=jdatetime.date.today(), user=request.user)
            Buy.save()
            messages.success(request, 'درخواست شما با موفقیت انجام شد')
            return redirect('withdrawalCustomer')
        else:
            messages.success(request, 'اسم شماره کارت با صاحب اکانت مطابقت ندارد')
            return redirect('settelmentCustomer')
    else:
        messages.success(request, 'در درخواست شما مشکلی پیش آمده است ')
        return redirect('withdrawalCustomer')


def changeGoldRequest(request):
    if request.method == 'POST':
        price = request.POST['price']
        gold = request.POST['gold']
        if gold == '':
            gold = 0
        elif price == '':
            price = 0
        if (float(gold) == 0 and int(price) != 0) or (int(price) == 0 and float(gold) != 0):
            if float(gold) > 99:
                messages.success(request, 'مقدار ظلا نمی تواند بیشتر از ۹۹ کیلو باشد')
                return redirect('ChangeGoldCustomer')
            else:
                Gold = convertGoldRequst(price=price, gold=gold, date=jdatetime.date.today(), user=request.user)
                Gold.save()
                messages.success(request, 'با موفقیت درخواست شما ثبت شد')
                return redirect('ChangeGoldCustomer')
        else:
            messages.success(request, 'یا باید مقدار ظلا رو بدید یا مقدار مبلغ هر ۲ همزمان انجام شدنی نیست')
            return redirect('ChangeGoldCustomer')
    else:
        messages.success(request, 'در ثبت درخواست شما مشکلی پیش آمده است')
        return redirect('ChangeGoldCustomer')


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
