# -*- coding: utf-8 -*-
"""
Standalone multiprocessing server
How to run:
python -O runserver.py
"""

import argparse
import logging
import logging.config
import sys
import os

import builtins

import bottle
from bottle import GeventServer
from TStore import TStoreApp


def install_routes():
    __import__('TStore.routes')


def setup_app(conf_file, bind_addr, bind_port):
    """
    Loads configurations from file
    :param conf_file: config file name
    :param bind_addr: bind address override
    :param bind_port: bind port override
    :return: (bind_address, bind_port)
    """
    app_config = TStoreApp.config
    app_config.load_config(conf_file)
    logging.config.fileConfig(app_config['server.logging_config'])

    builtins.LOGDEBUG = logging.getLogger('detail').debug
    builtins.LOGINFO = logging.getLogger('info').info
    builtins.LOGWARN = logging.getLogger('warn').warning
    builtins.LOGERR = logging.getLogger('error').error

    return bind_addr or app_config['server.listen_address'], bind_port or app_config['server.listen_port']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translations Store proxy server')
    parser.add_argument('config', nargs=1, type=str, help='Server configuration file path', default='./config.ini')
    parser.add_argument('--bind_address', type=str, help='Bind ip address', default='')
    parser.add_argument('--bind_port', type=str, help='Bind ip port', default='')
    args = parser.parse_args()

    conf_file = os.path.abspath(args.config[0])
    if not os.path.isfile(conf_file):
        raise IOError('File "{}" does not exist'.format(conf_file))
    bind_host, bind_port = setup_app(conf_file, args.bind_address, args.bind_port)

    install_routes()
    # run http server
    if TStoreApp.config['server.use_ssl'] == 'True':
        ssl_args = {
            'certfile': TStoreApp.config['server.ssl_certfile'],
            'keyfile': TStoreApp.config['server.ssl_keyfile'],
            'ssl_version': 2
        }
    else:
        ssl_args = {}

    LOGINFO('Listening on {}:{}'.format(bind_host, bind_port))
    bottle.run(app=TStoreApp, host=bind_host, port=bind_port, **ssl_args)
