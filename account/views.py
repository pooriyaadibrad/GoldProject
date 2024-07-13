from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from . import models
from django.contrib import messages
# Create your views here.
def signin(request):
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        user2 = User.objects.create_user(username=NationCode, password=password)
        user2.save()
        user1=models.user()
        user1.user=user2
        user1.save()
        login(request,user2)
        messages.success(request,'با موفقیت ثبت نام شدید')
        return redirect('adminCustome')
    else:
        return render(request,template_name='SignUp.html')
def Logout(request):
    logout(request)
    messages.success(request, 'خروج شما موفق بود!')
    return redirect('login')
def Login(request):
        return render(request,template_name='Login.html')


def LoginRequest(request):
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        user=authenticate(request,username=NationCode,password=password)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request,'با موفقیت وارد شدید!')
            return redirect('adminCustome')
        else:
            messages.success(request,'نام کاربری یا رمز عبور درست نمی باشد!')
            return render(request,template_name='Login.html')
    else:
        return render(request,template_name='Login.html')


def admin(request):
    return render(request,template_name='Admin.html')