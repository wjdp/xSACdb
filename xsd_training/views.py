from django.shortcuts import render, redirect
from django.template import RequestContext

from xsd_training.models import *

def overview(request):
    return render(request,'xsd_training/overview.html', context_instance=RequestContext(request))

def qualification_detail(request, id):
    qual=Qualification.objects.get(id=id)
    pass

def lesson_detail(request, id):
    pass

def sdc_list(request,id):
    pass
def sdc_detail(request,id):
    pass
