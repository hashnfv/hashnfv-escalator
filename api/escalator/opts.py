# Copyright (c) 2014 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import itertools

import escalator.api.middleware.context
import escalator.api.versions
import escalator.common.config
import escalator.common.rpc
import escalator.common.wsgi
import escalator.notifier

__all__ = [
    'list_api_opts',
]


_api_opts = [
    (None, list(itertools.chain(
        escalator.api.middleware.context.context_opts,
        escalator.api.versions.versions_opts,
        escalator.common.config.common_opts,
        escalator.common.rpc.rpc_opts,
        escalator.common.wsgi.bind_opts,
        escalator.common.wsgi.eventlet_opts,
        escalator.common.wsgi.socket_opts,
        escalator.notifier.notifier_opts))),
    ('task', escalator.common.config.task_opts),
    ('paste_deploy', escalator.common.config.paste_deploy_opts)
]


def list_api_opts():
    """Return a list of oslo.config options available in Escalator API service.

    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.

    This function is also discoverable via the 'escalator.api' entry point
    under the 'oslo.config.opts' namespace.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by escalator.

    :returns: a list of (group_name, opts) tuples
    """

    return [(g, copy.deepcopy(o)) for g, o in _api_opts]
