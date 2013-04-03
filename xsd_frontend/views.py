from django.shortcuts import render
from django.template import RequestContext

def dashboard(request):
    return render(request,'xsd_frontend/dashboard.html', {'request':request}, context_instance=RequestContext(request))
