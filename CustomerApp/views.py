import jdatetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from payment.models import paymentAccount, BuyRequst, sellRequst, convertGoldRequst
from account.models import person


# Create your views here.
def customer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            payment1 = paymentAccount.objects.get(user=request.user)
            Buy = BuyRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
            sell = sellRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
            Gold = convertGoldRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
            request1 = []
            request1.extend(Buy)
            request1.extend(sell)
            request1.extend(Gold)
            numberRequests = len(request1)
            daysTransactio = []
            lastInvoices1 = BuyRequst.objects.filter(user=request.user).all().order_by('-id')
            lastInvoices2 = sellRequst.objects.filter(user=request.user).all().order_by('-id')
            lastInvoices3 = convertGoldRequst.objects.filter(user=request.user).all().order_by('-id')
            lastInvoices = []
            try:
                lastInvoices1 = lastInvoices1[0:3]
                lastInvoices2 = lastInvoices2[0:3]
                lastInvoices3 = lastInvoices3[0:3]
            except IndexError:
                lastInvoices1 = lastInvoices1
                lastInvoices2 = lastInvoices2
                lastInvoices3 = lastInvoices3
            lastInvoices.extend(lastInvoices1)
            lastInvoices.extend(lastInvoices2)
            lastInvoices.extend(lastInvoices3)
            lastInvoices = sorted(lastInvoices, key=lambda x: x.date)
            lastInvoices.reverse()
            for i in lastInvoices1:
                if i.date == jdatetime.date.today():
                    daysTransactio.append(i)
            for j in lastInvoices2:
                if j.date == jdatetime.date.today():
                    daysTransactio.append(j)
            for k in lastInvoices3:
                if k.date == jdatetime.date.today():
                    daysTransactio.append(k)
            numberTransations = 0
            for transaction in daysTransactio:
                numberTransations = +transaction.price
            NumberdaysTransaction = 0
            for i in daysTransactio:
                NumberdaysTransaction += i.price

            return render(request=request, template_name='Dashbord.html',
                          context={'payment1': payment1, 'numberRequests': numberRequests,
                                   'numberTransations': numberTransations, 'lastInvoices': lastInvoices})
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            person1 = person.objects.get(user=request.user)
            account1 = paymentAccount.objects.get(user=request.user)
            return render(request=request, template_name='Profile.html',
                          context={'person1': person1, 'username': request.user.username, 'account': account1})
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')


def withdrawalCustomer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            buy = BuyRequst.objects.filter(user=request.user).all().order_by('-date')
            return render(request=request, template_name='withdrawal.html', context={'buy': buy})
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')


def settelmentCustomer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            user1 = User.objects.filter(is_superuser=True).first()
            payment1 = paymentAccount.objects.filter(user=user1).first()
            # payment2=paymentAccount.objects.filter(user=request.user).first()
            payment1 = [payment1.number, payment1.nameCart]
            sellrequst = sellRequst.objects.filter(user=request.user).all().order_by('-date')
            return render(request=request, template_name='Settlement.html',
                          context={'sellrequst': sellrequst, 'payment1': payment1})
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')


def ChangeGoldCustomer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            gold = convertGoldRequst.objects.filter(user=request.user).all().order_by('-date').order_by('-id')
            return render(request=request, template_name='ChengeToGoldCustomer.html', context={'gold': gold})
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')


def reportCustomer(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            return render(request=request, template_name='ReportCustomer.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')
