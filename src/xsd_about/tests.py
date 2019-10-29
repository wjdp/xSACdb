

from xSACdb.test_helpers import BaseTest, ViewTestMixin
from xsd_about.views import *

class AboutViewTest(ViewTestMixin, BaseTest):
    view = AboutView
    url_name = "xsd_about:AboutView"

class DatabaseOfficersViewTest(ViewTestMixin, BaseTest):
    view = DatabaseOfficersView
    url_name = "xsd_about:DatabaseOfficers"
