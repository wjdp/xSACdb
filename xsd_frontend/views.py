from django.shortcuts import render

def dashboard(request):
    return render(request,'xsd_frontend/dashboard.html')
