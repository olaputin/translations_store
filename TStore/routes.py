# -*- coding: utf-8 -*-
"""
routes definition file
"""

from __future__ import unicode_literals

import os
import re

from bottle import request

from TStore import TStoreApp


@TStoreApp.get('/resources/LanguagePackageItem/')
def get_resource():
    from bottle import static_file
    params = dict(request.query)
    code = ''.join(e for e in params.get('code', '') if e.isalnum()).upper()
    version = re.match('^(?:(\d+)\.)?(?:(\d+))', params.get('version', ''))
    if version:
        version = '.'.join(version.groups())
    lang_name = '{}.json'.format(code)
    root_dir = os.path.join('static', 'release', version, 'json')
    if os.path.exists(os.path.join(root_dir, lang_name)):
        return static_file(lang_name, root=root_dir, mimetype='application/json')

    root_dir = os.path.join('static', 'master', 'json')
    if os.path.exists(os.path.join(root_dir, lang_name)):
        return static_file(lang_name, root=root_dir, mimetype='application/json')

    return static_file('empty.json', root='', mimetype='application/json')
