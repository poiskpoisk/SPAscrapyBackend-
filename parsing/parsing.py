# -*- coding: utf-8 -*-#
__author__ = 'AMA'

import lxml.html as html
from urllib.request import urlopen, urlretrieve
from urllib.parse   import urlsplit
from .models import StatMsg, ParsingData, QueneURLs
from testjob2.settings import  BASE_DIR, STATIC_URL
import re
from .views import pendingFlag



