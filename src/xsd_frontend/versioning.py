from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property
from django.views.generic import ListView
from reversion.models import Version
from reversion_compare.mixins import CompareMixin


class XSDVersion(CompareMixin, Version):
    class Meta:
        proxy = True

    @property
    def cache_key(self):
        return 'version_{}'.format(self.pk)

    def _get_compare(self, obj_compare):
        # djang-reversion-compare has a stupid bug cos some things have no get_internal_type
        if not hasattr(obj_compare.field, 'get_internal_type'):
            # print("{} has no internal_type".format(obj_compare.field))
            return None
        # print("{} : {}".format(obj_compare.field, obj_compare.field.get_internal_type()))
        return super(XSDVersion, self)._get_compare(obj_compare)

    def all(self):
        """Return all versions for the object this version pertains to"""
        return XSDVersion.objects.get_for_object_reference(self._model, self.object_id)

    def compare_ForeignKey(self, obj_compare):
        """
        Simply create a html diff from the repr() result.
        Used for every field which has no own compare method.
        """
        value1, value2 = obj_compare.to_string()
        return "{} > {}".format(value1, value2)

    @cached_property
    def parent(self):
        """Get parent of this version"""
        try:
            return self.all().filter(pk__lt=self.pk).latest(field_name='revision__date_created')
        except ObjectDoesNotExist:
            return False

    def diff(self):
        """Return diff of this versions changes, returns None if root."""
        if self.parent:
            return self.compare(self.object, self.parent, self)[0]
        else:
            return None


class VersionHistoryView(ListView):
    model = XSDVersion
    template_name = 'versioning/history.html'
    context_object_name = 'versions'

    @cached_property
    def versioned_object(self):
        if hasattr(self, 'versioned_model'):
            return self.versioned_model.objects.get(pk=self.kwargs['pk'])
        else:
            return self.kwargs['model'].objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(VersionHistoryView, self).get_context_data(**kwargs)
        context['versioned_object'] = self.versioned_object
        context['page_title'] = 'Object History'
        return context

    def get_queryset(self):
        return XSDVersion.objects.get_for_object(self.versioned_object).select_related()


