from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from . import models
from payment.models import paymentAccount
from django.contrib import messages

from .models import person


# Create your views here.
def signin(request):
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        user=User.objects.filter(username=NationCode).all()
        if len(user) ==0:
            user2 = User.objects.create_user(username=NationCode, password=password)
            user2.save()
            user1=models.person()
            user1.user=user2
            user1.save()
            pamyment=paymentAccount(user=user2)
            pamyment.save()
            login(request,user2)
            messages.success(request,'با موفقیت ثبت نام شدید')
            return redirect('customerAPP')
        else:
            messages.success(request,'این کد ملی قبلا ثبت شده')
            return redirect('signin')
    else:
        return render(request, template_name='SignUp.html')
def Logout(request):
    logout(request)
    messages.success(request, 'خروج شما موفق بود!')
    return redirect('login')



def LoginRequest(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminAPP')
        else:
            return redirect('customerAPP')
    else:
        if request.method == 'POST':
            NationCode = request.POST['NationCode']
            password = request.POST['password']
            user=authenticate(request,username=NationCode,password=password)
            user1=User.objects.filter(username=NationCode).first()
            if user1 is not None:
                if user1.is_superuser:
                    login(request, user)
                    messages.success(request, 'ادمین با موفقیت وارد شدید!')
                    return redirect('adminAPP')
                else:
                    person=models.person.objects.get(user=user)
                    if user is not None:
                        if not person.blockStatus:
                            login(request,user)
                            messages.success(request,'با موفقیت وارد شدید!')
                            return redirect('customerAPP')
                        else:
                            messages.success(request, 'شما بلاک شدید لطفا با مدیریت تماس بگیرید')
                            return redirect('login')
                    else:
                        messages.success(request,'نام کاربری یا رمز عبور درست نمی باشد!')
                        return render(request, template_name='Login.html')
            else:
                messages.success(request,'اکانتی با                                                                                                                                                                                                                                                                                                                                          این مشخصات یافت نشد اگر اکانتی ندارید بسازید')
                return redirect('signin')
        else:
            return render(request, template_name='Login.html')



def DeleteCustomer(request,id):
    user = User.objects.get(id=id)
    person=models.person.objects.get(id=id)
    user.delete()
    person.delete()
    messages.success(request,'با موفقیت حذف شد')
    return redirect('userInfo')
def BlockCustomer(request,id):
    person=models.person.objects.get(id=id)
    person.blockStatus=True
    person.save()
    messages.success(request, 'با موفقیت مسدود شد')
    return redirect('userInfo')
def activeCustomer(request,id):
    person=models.person.objects.get(id=id)
    person.blockStatus=False
    person.save()
    messages.success(request,'با موفقیت کاربر فعال شد')
    return redirect('userInfo')
def changeBio(request):
    if request.method == 'POST':
        id=request.user.id
        user=User.objects.get(id=id)
        user1=person.objects.get(user=user)
        lineNumber = request.POST['lineNumber']
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        repassword = request.POST['repassword']
        address=request.POST['address']

        user1.address=address
        user1.LandlineNumber=lineNumber
        user.username=NationCode
        if password == repassword and password!='' and repassword!='':
            user.set_password(password)
        user.save()
        user1.save()
        login(request,user)
        messages.success(request,'تغغیرات با موفقیت اعمال شد')
        return redirect('changeBio')
    else:
        messages.success(request,'مشکلی ذر ثبت تغییرات پیش آمده است')
        return redirect('changeBio')
