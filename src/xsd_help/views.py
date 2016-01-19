import os
import json
import CommonMark

from django.views.generic import TemplateView
from django.conf import settings


class HelpView(TemplateView):
    template_name='help_page.html'
    doc_path = 'docs/'
    menu_file=os.path.join(settings.PROJECT_PATH, 'docs', 'menu.json')

    def get_page_name(self):
        if 'page' in self.kwargs:
            return self.kwargs['page']
        else:
            return 'index'

    def retrieve_page(self, page):
        try:
            with open(self.doc_path + page + '.md', 'r') as content_file:
                content = content_file.read()
            return content
        except IOError:
            return None

    def render_page(self, page):
        page_s = self.retrieve_page(page)
        if page_s:
            parser = CommonMark.DocParser()
            renderer = CommonMark.HTMLRenderer()
            ast = parser.parse(page_s)
            html = renderer.render(ast)
            return html
        else:
            return "<h1><i class='fa fa-warning error'></i> Page Not Found</h1><p>Whoops, the page " + page + " could not be found or is empty."

    def render_menu(self):
        with open(self.menu_file, 'r') as menu_file:
            menu_json = menu_file.read()
        menu = json.loads(menu_json)
        return menu


    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['page'] = self.render_page( self.get_page_name() )
        context['page_name'] = self.get_page_name()
        context['menu'] = self.render_menu()
        return context
