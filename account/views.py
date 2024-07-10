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
    if request.method == 'POST':
        NationCode = request.POST['NationCode']
        password = request.POST['password']
        user = authenticate(request, NationCode=NationCode, password=password)
        if user is not None:
            login(request, user)
            pass
    else:
        return render(request,template_name='Login.html')


