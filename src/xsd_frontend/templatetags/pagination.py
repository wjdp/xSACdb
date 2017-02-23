from django import template

register = template.Library()

def paginator(context, adjacent_pages=3):
    """
    To be used in conjunction with the object_list generic view.
    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page = context['page_obj']
    paginator = context['paginator']
    startPage = max(page.number - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = page.number + adjacent_pages + 1
    if endPage >= paginator.num_pages - 1: endPage = paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= paginator.num_pages]

    dict = {
        'request': context['request'],
        'is_paginated': paginator.num_pages > 0,
        'page_obj': page,
        'paginator': paginator,
        'results': paginator.per_page,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'first': 1,
        'last': paginator.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
    }

    if page.has_next():
        dict['next'] = page.next_page_number()
    if page.has_previous():
        dict['previous'] = page.previous_page_number()

    return dict

register.inclusion_tag('inclusion/pagination.html', takes_context=True)(paginator)
