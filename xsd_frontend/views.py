from django.shortcuts import render
from django.template import RequestContext

from datetime import date

def dashboard(request):
    now =date.today()
    p = request.user.get_profile()
    membership_ok=True
    no_data=False

    if p.club_expiry==None or p.bsac_expiry==None or p.medical_form_expiry==None:
        no_data=True
        membership_ok=False
        club_expired=True
        bsac_expired=True
        medical_form_expired=True
    else:
        if request.user.get_profile().club_expiry <= now:
            club_expired=True
            membership_ok=False
        else: club_expired=False
        if request.user.get_profile().bsac_expiry <= now:
            bsac_expired=True        
            membership_ok=False
        else: bsac_expired=False
        if request.user.get_profile().medical_form_expiry <= now:
            medical_form_expired=True        
            membership_ok=False
        else: medical_form_expired=False

    return render(request,'xsd_frontend/dashboard.html', {
        'request':request,
        'club_expired':club_expired,
        'bsac_expired':bsac_expired,
        'medical_form_expired':medical_form_expired,
        'no_data':no_data,
        'membership_ok':membership_ok,
    }, context_instance=RequestContext(request))
