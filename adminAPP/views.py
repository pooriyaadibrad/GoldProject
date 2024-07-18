from django.shortcuts import render,redirect
from account.models import User,person
from payment.models import paymentAccount,BuyRequst,sellRequst,convertGoldRequst
from django.contrib import messages
# Create your views here.
def admin(request):
    if request.user.is_authenticated:
        return render(request,template_name='Admin.html')
    else:
        messages.success(request,'لطفا اول وارد شوید')
        return redirect('login')
def cartNumber(request):
    if request.user.is_authenticated:
        return render(request=request,template_name='Cardnumber.html')
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
    users = person.objects.all()
    ResultUsers=[]
    for user1 in users:
        helpVaribaleForBuildUserInformation=[user1]
        payment=paymentAccount.objects.filter(user=user1.user).all()
        lastBuy=BuyRequst.objects.filter(user=user1.user).all().order_by('-id')
        lastSell=sellRequst.objects.filter(user=user1.user).all().order_by('-id')
        lastConvert=convertGoldRequst.objects.filter(user=user1.user).all().order_by('-id')
        if len(payment)>0:
            payment=payment[0]
            helpVaribaleForBuildUserInformation.append(payment.moneyInventory)
            helpVaribaleForBuildUserInformation.append(payment.goldInventory)
        else:
            helpVaribaleForBuildUserInformation.append('این کاربر حسابی ندارد')
        if len(lastBuy)>0 :
            lastBuy=lastBuy[0]
            helpVaribaleForBuildUserInformation.append(lastBuy.date)
        else:
            helpVaribaleForBuildUserInformation.append('خرید نداشت')
        if len(lastSell)>0 :
            lastSell=lastSell[0]
            helpVaribaleForBuildUserInformation.append(lastSell.date)
        else:
            helpVaribaleForBuildUserInformation.append('فروش نداشت')

        if len(lastConvert)>0 :
            lastConvert=lastConvert[0]
            helpVaribaleForBuildUserInformation.append(lastConvert.date)
        else:
            helpVaribaleForBuildUserInformation.append('خرید ظلا نداشت')
        ResultUsers.append(helpVaribaleForBuildUserInformation)
    return render(request=request,template_name='UserInfo-AdminPanel.html',context={'users':ResultUsers})
def withdrawal(request):
    return render(request=request,template_name='withdrawal-AdminPanel.html')