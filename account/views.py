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
        user1=models.user(NationCode=NationCode,password=password)
        user1.save()
        user2=User.objects.create_user(username=NationCode,password=password)
        user2.save()
        login(request,user2)
        return render(request,template_name='Admin.html')


    else:
        return render(request,template_name='SignUp.html')
def Logout(request):
    logout(request)
    return redirect('login')
def Login(request):
        return render(request,template_name='Login.html')


def LoginRequest(request):
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        user=authenticate(request,NationCode=NationCode,password=password)
        if user is not None:
            login(request,user)
            message=messages.success(request,'با موفقیت وارد شدید!')
            return redirect('admin')
        else:
            message=messages.success(request,'نام کاربری یا رمز عبور درست نمی باشد!')
            return render(request,template_name='Login.html',context={'message':message})


def admin(request):
    return render(request,template_name='Admin.html')