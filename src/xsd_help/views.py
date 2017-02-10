import os
import json
import CommonMark

from django.views.generic import TemplateView
from django.conf import settings


class HelpView(TemplateView):
    template_name = 'xsd_help/page.html'
    doc_path = os.path.join(settings.PROJECT_PATH, 'docs')
    menu_file = os.path.join(doc_path, 'menu.json')

    def get_page_name(self):
        if 'page' in self.kwargs:
            return self.kwargs['page']
        else:
            return 'index'

    def retrieve_page(self, page):
        page_path = os.path.join(self.doc_path, '{}.md'.format(page))
        try:
            with open(page_path, 'r') as content_file:
                content = content_file.read()
            return content
        except IOError:
            return None

    def render_page(self, page):
        page_s = self.retrieve_page(page)
        if page_s:
            parser = CommonMark.Parser()
            renderer = CommonMark.HtmlRenderer()
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
