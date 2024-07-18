from django.shortcuts import render

# Create your views here.
def admin(request):
    return render(request,template_name='Admin.html')
def cartNumber(request):
    return render(request=request,template_name='Cardnumber.html')
def changeToGold(request):
    return render(request=request,template_name='ChengeToGold.html')
def report(request):
    return render(request=request,template_name='Report.html')
def requestCustomer(request):
    return render(request=request,template_name='request.html')
def settlement(request):
    return render(request=request,template_name='settlement-AdminPanel.html')
def userInfo(request):
    return render(request=request,template_name='UserInfo-AdminPanel.html')
def withdrawal(request):
    return render(request=request,template_name='withdrawal-AdminPanel.html')