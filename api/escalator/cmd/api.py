#!/usr/bin/env python

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Escalator API Server
"""

import os
import sys

import eventlet

from oslo_service import systemd
from oslo_config import cfg
from oslo_log import log as logging
import osprofiler.notifier
import osprofiler.web

from escalator.common import config
from escalator.common import wsgi
from escalator import notifier


# Monkey patch socket, time, select, threads
eventlet.patcher.monkey_patch(all=False, socket=True, time=True,
                              select=True, thread=True, os=True)

# If ../escalator/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'escalator', '__init__.py')):
    sys.path.insert(0, possible_topdir)


CONF = cfg.CONF
CONF.import_group("profiler", "escalator.common.wsgi")
logging.register_options(CONF)


def fail(e):
    sys.exit(100)


def main():
    try:
        config.parse_args()
        wsgi.set_eventlet_hub()
        logging.setup(CONF, 'escalator')

        if cfg.CONF.profiler.enabled:
            _notifier = osprofiler.notifier.create("Messaging",
                                                   notifier.messaging, {},
                                                   notifier.get_transport(),
                                                   "escalator", "api",
                                                   cfg.CONF.bind_host)
            osprofiler.notifier.set(_notifier)
        else:
            osprofiler.web.disable()

        server = wsgi.Server()
        server.start(config.load_paste_app('escalator-api'), default_port=9393)
        systemd.notify_once()
        server.wait()
    except Exception as e:
        fail(e)


if __name__ == '__main__':
    main()
