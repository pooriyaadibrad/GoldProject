from inspect import stack

import jdatetime
from jdatetime import timedelta
from django.shortcuts import render, redirect

from CustomerApp.views import customer
from account.models import User, person
from payment.models import paymentAccount, BuyRequst, sellRequst, convertGoldRequst, ConvertMoneyRequst, GetGoldRequst, \
    Invoice, paymentDate
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            invoicesNumber = Invoice.objects.filter(status=0).all()
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            invoicesNumber = len(invoicesNumber)
            user = User.objects.filter(is_superuser=True).all()
            user = user[0]
            payment = paymentAccount.objects.filter(user=user).all()
            try:
                payment = payment[0]
            except IndexError:
                payment = None

            if payment == None:
                messages.success(request,
                                 'شما حساب کاربری ندارید یکی باید حتما بسازید / با تیم فنی تماس بگیرید در اسرع وقت بابت این موضوع')
                return render(request, template_name='Admin.html',
                              context={'invoicesNumber': invoicesNumber, 'payment': payment})
            else:
                lastInvoices1 = BuyRequst.objects.filter(status=2).all().order_by('-id')
                lastInvoices2 = sellRequst.objects.filter(status=2).all().order_by('-id')
                lastInvoices3 = convertGoldRequst.objects.filter(status=2).all().order_by('-id')
                lastInvoices4 = ConvertMoneyRequst.objects.filter(status=2).all().order_by('-id')

                last4daysTransaction = []

                for p in range(4):
                    daysTransactio = []

                    for i in lastInvoices1:
                        if i.date == jdatetime.date.today() - timedelta(days=p):
                            daysTransactio.append(i)
                    for j in lastInvoices2:
                        if j.date == jdatetime.date.today() - timedelta(days=p):
                            daysTransactio.append(j)
                    for k in lastInvoices3:
                        if k.date == jdatetime.date.today() - timedelta(days=p):
                            daysTransactio.append(k)

                    for u in lastInvoices4:
                        if u.date == jdatetime.date.today() - timedelta(days=p):
                            daysTransactio.append(u)

                    NumberdaysTransaction = 0
                    for i in daysTransactio:
                        NumberdaysTransaction += i.price

                    last4daysTransaction.append(NumberdaysTransaction)
                day_gold = []
                day_gold.extend(lastInvoices3)
                day_gold.extend(lastInvoices4)
                gold = 0
                for i in day_gold:
                    gold += i.gold
                lastInvoices1 = BuyRequst.objects.filter(status=0).all().order_by('-id')
                lastInvoices2 = sellRequst.objects.filter(status=0).all().order_by('-id')
                lastInvoices3 = convertGoldRequst.objects.filter(status=0).all().order_by('-id')
                lastInvoices4 = ConvertMoneyRequst.objects.filter(status=0).all().order_by('-id')
                lastInvoices5 = GetGoldRequst.objects.filter(status=0).all().order_by('-id')
                lastInvoices = []
                try:
                    lastInvoices.extend(lastInvoices1[0:3])
                    lastInvoices.extend(lastInvoices2[0:3])
                    lastInvoices.extend(lastInvoices3[0:3])
                    lastInvoices.extend(lastInvoices4[0:3])
                    lastInvoices.extend(lastInvoices5[0:3])
                except IndexError:
                    lastInvoices.extend(lastInvoices1)
                    lastInvoices.extend(lastInvoices2)
                    lastInvoices.extend(lastInvoices3)
                    lastInvoices.extend(lastInvoices4)
                    lastInvoices.extend(lastInvoices5)

                lastInvoices = sorted(lastInvoices, key=lambda obj: obj.date)
                if len(lastInvoices) > 6:
                    lastInvoices = lastInvoices[0:6]
                for item in lastInvoices:
                    user1 = person.objects.filter(user=item.user).first()
                    lastInvoices[lastInvoices.index(item)] = [item, user1.Mobile]

                dayesX = []
                for i in range(0, 4):
                    calendarLine = jdatetime.date.today() - timedelta(days=i)
                    dayesX.append(calendarLine.strftime('%Y-%m-%d'))
                new_persons = person.objects.filter(new_customer_status=True).all()
                return render(request, template_name='Admin.html',
                              context={'invoicesNumber': invoicesNumber, 'payment': payment,
                                       'lastInvoices': lastInvoices, 'last4daysTransaction': last4daysTransaction,
                                       'dayesX': dayesX, 'paymentDate': paymentDate1, 'gold_day': gold,
                                       'new_persons': len(new_persons)})
        else:

            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def cartNumber(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            payment = paymentAccount.objects.filter(user=request.user).first()
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            return render(request=request, template_name='Cardnumber.html',
                          context={'payment': payment, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def changeToGold(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            Gold = convertGoldRequst.objects.all().order_by('-date')
            Gold1 = []
            Gold1.extend(Gold)
            i = 0
            for b in Gold1:
                user1 = person.objects.filter(user=b.user).first()
                payment = paymentAccount.objects.filter(user=b.user).first()
                Gold1[i] = [b, user1, payment]
                i += 1
            if len(Gold1) > 10:
                Gold1 = Gold1[0:10]

            return render(request=request, template_name='ChengeToGold.html',
                          context={'Gold': Gold1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def report(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            return render(request=request, template_name='Report.html',
                          context={'data': [], 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def requestCustomer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            Buy = BuyRequst.objects.filter(status=0).all().order_by('-id')
            sell = sellRequst.objects.filter(status=0).all().order_by('-id')
            gold = convertGoldRequst.objects.filter(status=0).all().order_by('-id')
            money = ConvertMoneyRequst.objects.filter(status=0).all().order_by('-id')
            get_gold = GetGoldRequst.objects.filter(status=0).all().order_by('-id')
            requestCustomer1 = []
            requestCustomer1.extend(Buy)
            requestCustomer1.extend(sell)
            requestCustomer1.extend(gold)
            requestCustomer1.extend(money)
            requestCustomer1.extend(get_gold)
            i = 0
            for req in requestCustomer1:
                user1 = person.objects.filter(user=req.user).first()
                payment = paymentAccount.objects.filter(user=req.user).first()
                requestCustomer1[i] = [req, user1, payment]
                i += 1
            return render(request=request, template_name='request.html',
                          context={'requestCustomer': requestCustomer1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def settlement(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            sell = sellRequst.objects.all().order_by('-date')
            sell1 = []
            sell1.extend(sell)
            i = 0
            for b in sell1:
                user1 = person.objects.filter(user=b.user).first()
                payment = paymentAccount.objects.filter(user=b.user).first()
                sell1[i] = [b, user1, payment]
                i += 1
            if len(sell) > 10:
                sell1 = sell1[0:10]

            return render(request=request, template_name='settlement-AdminPanel.html',
                          context={'sell': sell1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def userInfo(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            users = User.objects.filter(is_superuser=False).all()
            ResultUsers = []
            for user1 in users:
                helpVaribaleForBuildUserInformation = [user1]
                payment = paymentAccount.objects.filter(user=user1).all()
                lastBuy = BuyRequst.objects.filter(user=user1).all().order_by('-id')
                lastSell = sellRequst.objects.filter(user=user1).all().order_by('-id')
                lastConvert = convertGoldRequst.objects.filter(user=user1).all().order_by('-id')
                person1 = person.objects.filter(user=user1).first()
                if len(payment) > 0:
                    payment = payment[0]
                    helpVaribaleForBuildUserInformation.append(payment.moneyInventory)
                    helpVaribaleForBuildUserInformation.append(payment.goldInventory)
                else:
                    helpVaribaleForBuildUserInformation.append('این کاربر حسابی ندارد')
                if len(lastBuy) > 0:
                    lastBuy = lastBuy[0]
                    helpVaribaleForBuildUserInformation.append(lastBuy.date)
                else:
                    helpVaribaleForBuildUserInformation.append('خرید نداشت')
                if len(lastSell) > 0:
                    lastSell = lastSell[0]
                    helpVaribaleForBuildUserInformation.append(lastSell.date)
                else:
                    helpVaribaleForBuildUserInformation.append('فروش نداشت')

                if len(lastConvert) > 0:
                    lastConvert = lastConvert[0]
                    helpVaribaleForBuildUserInformation.append(lastConvert.date)
                else:
                    helpVaribaleForBuildUserInformation.append('خرید طلا نداشت')
                helpVaribaleForBuildUserInformation.append(person1.Mobile)
                helpVaribaleForBuildUserInformation.append(person1.blockStatus)
                helpVaribaleForBuildUserInformation.append(person1.picture)
                helpVaribaleForBuildUserInformation.append(person1.new_customer_status)
                ResultUsers.append(helpVaribaleForBuildUserInformation)
            ResultUsers.reverse()
            return render(request=request, template_name='UserInfo-AdminPanel.html',
                          context={'users': ResultUsers, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def withdrawal(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            Buy = BuyRequst.objects.all().order_by('-date')
            Buy1 = []
            Buy1.extend(Buy)
            i = 0
            for b in Buy1:
                user1 = person.objects.filter(user=b.user).first()
                payment = paymentAccount.objects.filter(user=b.user).first()
                Buy1[i] = [b, user1, payment]
                i += 1
            if len(Buy1) > 10:
                Buy1 = Buy1[0:10]

            return render(request=request, template_name='withdrawal-AdminPanel.html',
                          context={'Buy': Buy1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def ConvertMoneyRequest(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            moneyRequst = ConvertMoneyRequst.objects.all().order_by('-date')
            Buy1 = []
            Buy1.extend(moneyRequst)
            i = 0
            for b in Buy1:
                user1 = person.objects.filter(user=b.user).first()
                payment = paymentAccount.objects.filter(user=b.user).first()
                Buy1[i] = [b, user1, payment]
                i += 1
            if len(Buy1) > 10:
                Buy1 = Buy1[0:10]

            return render(request=request, template_name='ConvertToMoney.html',
                          context={'money': Buy1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def GetGoldRequest(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            GetGoldRequst1 = GetGoldRequst.objects.all().order_by('-date')
            Buy1 = []
            Buy1.extend(GetGoldRequst1)
            i = 0
            for b in Buy1:
                user1 = person.objects.filter(user=b.user).first()
                payment = paymentAccount.objects.filter(user=b.user).first()
                Buy1[i] = [b, user1, payment]
                i += 1
            if len(Buy1) > 10:
                Buy1 = Buy1[0:10]

            return render(request=request, template_name='getGold.html',
                          context={'getGold': Buy1, 'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def DeterminingGoldPrice(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                DayPrice = request.POST.get('DayPrice')
                paymentDate1 = paymentDate.objects.create(price=DayPrice)
                paymentDate1.save()
                return redirect('DeterminingGoldPrice')
            else:
                try:
                    paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
                except IndexError:
                    paymentDate1 = paymentDate.objects.all().order_by('-id')
                return render(request=request, template_name='NerkhTala.html', context={'paymentDate': paymentDate1})
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def search_customer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            try:
                paymentDate1 = paymentDate.objects.all().order_by('-id')[0]
            except IndexError:
                paymentDate1 = paymentDate.objects.all().order_by('-id')
            query = request.POST.get('search')
            if query:
                if query[0] != '0':
                    users = User.objects.filter(
                        Q(is_superuser=False) & Q(first_name__icontains=query) | Q(username__icontains=query)).all()
                    ResultUsers = []
                    print(users)
                    for user1 in users:
                        helpVaribaleForBuildUserInformation = [user1]
                        payment = paymentAccount.objects.filter(user=user1).all()
                        lastBuy = BuyRequst.objects.filter(user=user1).all().order_by('-id')
                        lastSell = sellRequst.objects.filter(user=user1).all().order_by('-id')
                        lastConvert = convertGoldRequst.objects.filter(user=user1).all().order_by('-id')
                        person1 = person.objects.filter(user=user1).first()
                        print(person1)
                        if len(payment) > 0:
                            payment = payment[0]
                            helpVaribaleForBuildUserInformation.append(payment.moneyInventory)
                            helpVaribaleForBuildUserInformation.append(payment.goldInventory)
                        else:
                            helpVaribaleForBuildUserInformation.append('این کاربر حسابی ندارد')
                        if len(lastBuy) > 0:
                            lastBuy = lastBuy[0]
                            helpVaribaleForBuildUserInformation.append(lastBuy.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('خرید نداشت')
                        if len(lastSell) > 0:
                            lastSell = lastSell[0]
                            helpVaribaleForBuildUserInformation.append(lastSell.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('فروش نداشت')

                        if len(lastConvert) > 0:
                            lastConvert = lastConvert[0]
                            helpVaribaleForBuildUserInformation.append(lastConvert.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('خرید طلا نداشت')
                        try:
                            helpVaribaleForBuildUserInformation.append(person1.Mobile)
                            helpVaribaleForBuildUserInformation.append(person1.blockStatus)
                            helpVaribaleForBuildUserInformation.append(person1.picture)
                        except AttributeError:
                            helpVaribaleForBuildUserInformation.append('این یوزر نباید اجازه فعالیت داشته باشید')
                            helpVaribaleForBuildUserInformation.append('این یوزر نباید اجازه فعالیت داشته باشید')
                            helpVaribaleForBuildUserInformation.append('این یوزر نباید اجازه فعالیت داشته باشید')

                        ResultUsers.append(helpVaribaleForBuildUserInformation)
                    ResultUsers.reverse()
                    return render(request=request, template_name='UserInfo-AdminPanel.html',
                                  context={'users': ResultUsers, 'paymentDate': paymentDate1})
                else:
                    persons = person.objects.filter(Q(Mobile=query)).all()
                    stack_user = []
                    ResultUsers = []
                    for pers in persons:
                        stack_user.append(pers.user)
                    for user1 in stack_user:
                        user1 = User.objects.filter(username=user1.username).first()
                        helpVaribaleForBuildUserInformation = [user1]
                        payment = paymentAccount.objects.filter(user=user1).all()
                        lastBuy = BuyRequst.objects.filter(user=user1).all().order_by('-id')
                        lastSell = sellRequst.objects.filter(user=user1).all().order_by('-id')
                        lastConvert = convertGoldRequst.objects.filter(user=user1).all().order_by('-id')
                        person1 = person.objects.filter(user=user1).first()
                        if len(payment) > 0:
                            payment = payment[0]
                            helpVaribaleForBuildUserInformation.append(payment.moneyInventory)
                            helpVaribaleForBuildUserInformation.append(payment.goldInventory)
                        else:
                            helpVaribaleForBuildUserInformation.append('این کاربر حسابی ندارد')
                        if len(lastBuy) > 0:
                            lastBuy = lastBuy[0]
                            helpVaribaleForBuildUserInformation.append(lastBuy.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('خرید نداشت')
                        if len(lastSell) > 0:
                            lastSell = lastSell[0]
                            helpVaribaleForBuildUserInformation.append(lastSell.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('فروش نداشت')

                        if len(lastConvert) > 0:
                            lastConvert = lastConvert[0]
                            helpVaribaleForBuildUserInformation.append(lastConvert.date)
                        else:
                            helpVaribaleForBuildUserInformation.append('خرید طلا نداشت')
                        helpVaribaleForBuildUserInformation.append(person1.Mobile)
                        helpVaribaleForBuildUserInformation.append(person1.blockStatus)
                        helpVaribaleForBuildUserInformation.append(person1.picture)

                        ResultUsers.append(helpVaribaleForBuildUserInformation)
                    ResultUsers.reverse()
                    return render(request=request, template_name='UserInfo-AdminPanel.html',
                                  context={'users': ResultUsers, 'paymentDate': paymentDate1})
            else:
                return redirect('userInfo')
        else:
            messages.success(request, 'لطفا اول با اکانت ادمین وارد شوید')
            return redirect('login')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')
