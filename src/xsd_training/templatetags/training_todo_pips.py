from django import template

from xsd_training.views.support import TrainingUpdateRequestList

register = template.Library()

@register.simple_tag
def todo_bool(item):
    if item == 'TrainingUpdateRequestList':
        return todo('TrainingUpdateRequestList')>0


@register.simple_tag
def todo(item):
    if item == 'TrainingUpdateRequestList':
        view = TrainingUpdateRequestList()
        x = TrainingUpdateRequestList.get_queryset(view).filter(completed=False, area='tra').count()
        if x>0:
            return '<div class="pull-right badge badge-important">'+str(x)+'</div>'
        else: return ""
