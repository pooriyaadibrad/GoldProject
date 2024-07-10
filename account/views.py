from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
# Create your views here.
def signin(request):
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        pass
def Logout(request):
    logout(request)
    pass
def Login(request):
        return render(request,template_name='Login.html',context={'NationCode':'NationCode','password':'password'})


def LoginRequest(request):
    print('this is test')
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        return render(request, 'Login.html',{'NationCode':NationCode,'password':password})

