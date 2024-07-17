from django.shortcuts import render

# Create your views here.
def cartNumber(request):
    return render(request=request,template_name='Cardnumber.html')
def changeToGold(request):
    return render(request=request,template_name='ChengeToGold.html')