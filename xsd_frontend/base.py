from django.views.generic.base import View
from django.views.generic.list import ListView

from django.shortcuts import redirect

from models import UpdateRequest
from forms import UpdateRequestReply

class BaseUpdateRequestList(ListView):
    model=UpdateRequest
    template_name=""    # Must be set by child views
    area=""             # Again set by child view
    form_action=""      # Where to send the form
    custom_include=""
    context_object_name="update_requests" # This is consistant

    def get_queryset(self):
        queryset=super(BaseUpdateRequestList, self).get_queryset()
        queryset=queryset.filter(area=self.area).order_by('-sent')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(BaseUpdateRequestList, self).get_context_data(**kwargs)
        context['response_form'] = UpdateRequestReply()
        context['form_action']=self.form_action
        context['update_request_custom']=self.custom_include
        return context

class BaseUpdateRequestRespond(View):
    success_url=""  # Where to return, the UpdateRequestList is a good bet

    def post(self,request, *args, **kwargs):
        ur_pk=int(request.POST['pk'])
        ur=UpdateRequest.objects.get(pk=ur_pk)
        ur.response_body=request.POST['response_body']
        if 'completed' in request.POST: ur.completed=request.POST['completed']
        if ur.completed and 'completed' not in request.POST: ur.completed=False
        ur.save()
        return_url=self.success_url+"#ur"+str(ur_pk)
        return redirect(return_url)