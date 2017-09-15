# -*- coding: utf-8 -*-
"""
routes definition file
"""

from __future__ import unicode_literals

from TStore import TStoreApp
from bottle import request

# /resources/LanguagePackageItem/?format=json&limit=0&establishment=323&code=_SP

@TStoreApp.get('/resources/LanguagePackageItem/')
def get_resource():
    print(request)
    return 'OK'
