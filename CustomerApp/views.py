from django.shortcuts import render,redirect
from django.contrib import messages
from payment.models import paymentAccount,BuyRequst,sellRequst,convertGoldRequst
# Create your views here.
def customer(request):
    if request.user.is_authenticated:
        payment1=paymentAccount.objects.get(user=request.user)
        Buy=BuyRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
        sell=sellRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
        Gold=convertGoldRequst.objects.filter(user=request.user).filter(status=0).all().order_by('-id')
        request1=[]
        request1.extend(Buy)
        request1.extend(sell)
        request1.extend(Gold)
        numberRequests=len(request1)
        return render(request=request,template_name='Dashbord.html',context={'payment1':payment1,'numberRequests':numberRequests})
    else:
        messages.success(request,'لظفا اول وارد شوید')
        return redirect('login')
def profile(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='Profile.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')
def withdrawalCustomer(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='withdrawal.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')
def settelmentCustomer(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='Settlement.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')
def ChangeGoldCustomer(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='ChengeToGoldCustomer.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')
def reportCustomer(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='ReportCustomer.html')
    else:
        messages.success(request, 'لظفا اول وارد شوید')
        return redirect('login')