from __future__ import absolute_import

import os

if 'XSACDB_ENVIRONMENT' in os.environ and os.environ['XSACDB_ENVIRONMENT']=='PRODUCTION':
    from .production import *
else:
    from .development import *
