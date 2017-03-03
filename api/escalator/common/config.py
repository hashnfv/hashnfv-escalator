
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
Routines for configuring Escalator
"""

import logging
import logging.config
import logging.handlers
import os
import tempfile

from oslo_concurrency import lockutils
from oslo_config import cfg
from oslo_policy import policy
from paste import deploy

from escalator import i18n
from escalator.version import version_info as version

_ = i18n._

paste_deploy_opts = [
    cfg.StrOpt('flavor',
               help=_('Partial name of a pipeline in your paste configuration '
                      'file with the service name removed. For example, if '
                      'your paste section name is '
                      '[pipeline:escalator-api-keystone] use the value '
                      '"keystone"')),
    cfg.StrOpt('config_file',
               help=_('Name of the paste configuration file.')),
]
task_opts = [
    cfg.IntOpt('task_time_to_live',
               default=48,
               help=_("Time in hours for which a task lives after, either "
                      "succeeding or failing"),
               deprecated_opts=[cfg.DeprecatedOpt('task_time_to_live',
                                                  group='DEFAULT')]),
    cfg.StrOpt('task_executor',
               default='taskflow',
               help=_("Specifies which task executor to be used to run the "
                      "task scripts.")),
    cfg.StrOpt('work_dir',
               default=None,
               help=_('Work dir for asynchronous task operations. '
                      'The directory set here will be used to operate over '
                      'images - normally before they are imported in the '
                      'destination store. When providing work dir, make sure '
                      'enough space is provided for concurrent tasks to run '
                      'efficiently without running out of space. A rough '
                      'estimation can be done by multiplying the number of '
                      '`max_workers` - or the N of workers running - by an '
                      'average image size (e.g 500MB). The image size '
                      'estimation should be done based on the average size in '
                      'your deployment. Note that depending on the tasks '
                      'running you may need to multiply this number by some '
                      'factor depending on what the task does. For example, '
                      'you may want to double the available size if image '
                      'conversion is enabled. All this being said, remember '
                      'these are just estimations and you should do them '
                      'based on the worst case scenario and be prepared to '
                      'act in case they were wrong.')),
]
common_opts = [
    cfg.IntOpt('limit_param_default', default=25,
               help=_('Default value for the number of items returned by a '
                      'request if not specified explicitly in the request')),
    cfg.IntOpt('api_limit_max', default=1000,
               help=_('Maximum permissible number of items that could be '
                      'returned by a request')),
    cfg.BoolOpt('enable_v1_api', default=True,
                help=_("Deploy the v1 OPNFV  Escalator API.")),
    cfg.BoolOpt('enable_v2_api', default=True,
                help=_("Deploy the v2 OpenStack Images API.")),
    cfg.StrOpt('pydev_worker_debug_host',
               help=_('The hostname/IP of the pydev process listening for '
                      'debug connections')),
    cfg.IntOpt('pydev_worker_debug_port', default=5678,
               help=_('The port on which a pydev process is listening for '
                      'connections.')),
    cfg.StrOpt('digest_algorithm', default='sha1',
               help=_('Digest algorithm which will be used for digital '
                      'signature; the default is sha1 the default in Kilo '
                      'for a smooth upgrade process, and it will be updated '
                      'with sha256 in next release(L). Use the command '
                      '"openssl list-message-digest-algorithms" to get the '
                      'available algorithms supported by the version of '
                      'OpenSSL on the platform. Examples are "sha1", '
                      '"sha256", "sha512", etc.')),
]

CONF = cfg.CONF
CONF.register_opts(paste_deploy_opts, group='paste_deploy')
CONF.register_opts(task_opts, group='task')
CONF.register_opts(common_opts)
policy.Enforcer(CONF)


def parse_args(args=None, usage=None, default_config_files=None):
    if "OSLO_LOCK_PATH" not in os.environ:
        lockutils.set_defaults(tempfile.gettempdir())

    CONF(args=args,
         project='escalator',
         version=version.cached_version_string(),
         usage=usage,
         default_config_files=default_config_files)


def _get_deployment_flavor(flavor=None):
    """
    Retrieve the paste_deploy.flavor config item, formatted appropriately
    for appending to the application name.

    :param flavor: if specified, use this setting rather than the
                   paste_deploy.flavor configuration setting
    """
    if not flavor:
        flavor = CONF.paste_deploy.flavor
    return '' if not flavor else ('-' + flavor)


def _get_paste_config_path():
    paste_suffix = '-paste.ini'
    conf_suffix = '.conf'
    if CONF.config_file:
        # Assume paste config is in a paste.ini file corresponding
        # to the last config file
        path = CONF.config_file[-1].replace(conf_suffix, paste_suffix)
    else:
        path = CONF.prog + paste_suffix
    return CONF.find_file(os.path.basename(path))


def _get_deployment_config_file():
    """
    Retrieve the deployment_config_file config item, formatted as an
    absolute pathname.
    """
    path = CONF.paste_deploy.config_file
    if not path:
        path = _get_paste_config_path()
    if not path:
        msg = _("Unable to locate paste config file for %s.") % CONF.prog
        raise RuntimeError(msg)
    return os.path.abspath(path)


def load_paste_app(app_name, flavor=None, conf_file=None):
    """
    Builds and returns a WSGI app from a paste config file.

    We assume the last config file specified in the supplied ConfigOpts
    object is the paste config file, if conf_file is None.

    :param app_name: name of the application to load
    :param flavor: name of the variant of the application to load
    :param conf_file: path to the paste config file

    :raises RuntimeError when config file cannot be located or application
            cannot be loaded from config file
    """
    # append the deployment flavor to the application name,
    # in order to identify the appropriate paste pipeline
    app_name += _get_deployment_flavor(flavor)

    if not conf_file:
        conf_file = _get_deployment_config_file()

    try:
        logger = logging.getLogger(__name__)
        logger.debug("Loading %(app_name)s from %(conf_file)s",
                     {'conf_file': conf_file, 'app_name': app_name})

        app = deploy.loadapp("config:%s" % conf_file, name=app_name)

        # Log the options used when starting if we're in debug mode...
        if CONF.debug:
            CONF.log_opt_values(logger, logging.DEBUG)

        return app
    except (LookupError, ImportError) as e:
        msg = (_("Unable to load %(app_name)s from "
                 "configuration file %(conf_file)s."
                 "\nGot: %(e)r") % {'app_name': app_name,
                                    'conf_file': conf_file,
                                    'e': e})
        logger.error(msg)
        raise RuntimeError(msg)
