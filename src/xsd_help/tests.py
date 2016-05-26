from __future__ import unicode_literals

from xSACdb.test_helpers import BaseTest, ViewTestMixin
from xsd_help.views import HelpView

class HelpViewTest(ViewTestMixin, BaseTest):
    view = HelpView
    url_name = 'xsd_help:HelpView'
    allowed_unverified = True

    def test_menu(self):
        helpView = HelpView()
        self.assertIsInstance(helpView.render_menu(), dict)

    def test_render_help_page(self):
        helpView = HelpView()

        for section in helpView.render_menu()['sections']:
            for link in section['links']:
                url = '/help/{0}/'.format(link[1])
                self.assert200(url)

    def test_page_not_found(self):
        url = '/help/not-a-real-page/'
        c = self.get_client()
        response = c.get(url)
        self.assertContains(response, "Page Not Found")
