from django.views.generic.list import ListView

class OrderedListView(ListView):
    def get_queryset(self):
        return super(OrderedListView, self).get_queryset().order_by(self.order_by)

class UserContextMixin():
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserContextMixin, self).get_context_data(**kwargs)
        # Add in the logged in user
        context['user'] = self.request.user
        return context