from django.core.exceptions import ViewDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView


class OrderedListView(ListView):
    def get_queryset(self):
        return super(OrderedListView, self).get_queryset().order_by(self.order_by)


class ActionView(SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        func = getattr(self, self.kwargs['action'], None)
        if func:
            ret = func(request)
            return redirect(ret or self.get_object())
        else:
            raise ViewDoesNotExist('You ain\'t got a func in your trunk!')


