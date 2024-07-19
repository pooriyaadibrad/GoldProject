import jdatetime
from jdatetime import timedelta
from django.shortcuts import render,redirect
from account.models import User,person
from payment.models import paymentAccount,BuyRequst,sellRequst,convertGoldRequst,Invoice
from django.contrib import messages
# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        invoicesNumber=Invoice.objects.filter(status=False).all()

        invoicesNumber=len(invoicesNumber)
        user=User.objects.filter(is_superuser=True).all()
        user=user[0]
        payment=paymentAccount.objects.filter(user=user).all()
        try:
            payment=payment[0]
        except IndexError:
            payment=None

        if payment==None:
            messages.success(request,'شما حساب کاربری ندارید یکی باید حتما بسازید / با تیم فنی تماس بگیرید در اسرع وقت بابت این موضوع')
            return render(request, template_name='Admin.html', context={'invoicesNumber': invoicesNumber, 'payment': payment})
        else:
            lastInvoices1 = BuyRequst.objects.filter(status=True).all().order_by('-id')
            lastInvoices2= sellRequst.objects.filter(status=True).all().order_by('-id')
            lastInvoices3 = convertGoldRequst.objects.filter(status=True).all().order_by('-id')
            last4daysTransaction=[]
            for p in range(4):
                daysTransactio=[]
                for i in lastInvoices1:
                    if i.date == jdatetime.date.today() - timedelta(days=p):
                        daysTransactio.append(i)
                for j in lastInvoices2:
                    if j.date == jdatetime.date.today() - timedelta(days=p):

                        daysTransactio.append(j)
                for k in lastInvoices3:
                    if k.date == jdatetime.date.today() - timedelta(days=p):
                        daysTransactio.append(k)

                NumberdaysTransaction=0
                for i in daysTransactio:
                    NumberdaysTransaction+=i.price
                last4daysTransaction.append(NumberdaysTransaction)

            lastInvoices = []
            try:
                lastInvoices.extend(lastInvoices1[0:3])
                lastInvoices.extend(lastInvoices2[0:3])
                lastInvoices.extend(lastInvoices3[0:3])
            except IndexError:
                lastInvoices.extend(lastInvoices1)
                lastInvoices.extend(lastInvoices2)
                lastInvoices.extend(lastInvoices3)

            lastInvoices=sorted(lastInvoices , key=lambda obj:obj.date)
            for item in lastInvoices:
                user1=person.objects.filter(user=item.user).first()
                lastInvoices[lastInvoices.index(item)] = [item,user1.Mobile]

            dayesX = []
            for i in range(0, 4):
                calendarLine = jdatetime.date.today() - timedelta(days=i)
                dayesX.append(calendarLine.strftime('%Y-%m-%d'))
            return render(request,template_name='Admin.html',context={'invoicesNumber':invoicesNumber,'payment':payment,'lastInvoices':lastInvoices,'last4daysTransaction':last4daysTransaction,'dayesX':dayesX})
    else:
        messages.success(request,'لطفا اول وارد شوید')
        return redirect('login')
def cartNumber(request):
    if request.user.is_authenticated:
        payment=paymentAccount.objects.filter(user=request.user).first()
        return render(request=request,template_name='Cardnumber.html',context={'payment':payment})
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')

def changeToGold(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='ChengeToGold.html')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')

def report(request):
    if request.user.is_authenticated:
        return render(request=request,template_name='Report.html')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')

def requestCustomer(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='request.html')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')

def settlement(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='settlement-AdminPanel.html')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')


def userInfo(request):
    if request.user.is_authenticated:
        users = person.objects.all()
        ResultUsers = []
        for user1 in users:
            helpVaribaleForBuildUserInformation = [user1]
            payment = paymentAccount.objects.filter(user=user1.user).all()
            lastBuy = BuyRequst.objects.filter(user=user1.user).all().order_by('-id')
            lastSell = sellRequst.objects.filter(user=user1.user).all().order_by('-id')
            lastConvert = convertGoldRequst.objects.filter(user=user1.user).all().order_by('-id')
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
                helpVaribaleForBuildUserInformation.append('خرید ظلا نداشت')
            ResultUsers.append(helpVaribaleForBuildUserInformation)
        return render(request=request, template_name='UserInfo-AdminPanel.html', context={'users': ResultUsers})
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')



def withdrawal(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='withdrawal-AdminPanel.html')
    else:
        messages.success(request, 'لطفا اول وارد شوید')
        return redirect('login')

