# Copyright 2013 OpenStack Foundation
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
/hosts endpoint for Daisy v1 API
"""

from oslo_log import log as logging
from webob.exc import HTTPBadRequest

from escalator import i18n
from escalator import notifier

from escalator.api import policy
import escalator.api.v1
from escalator.common import exception
from escalator.common import utils
from escalator.common import wsgi
from escalator.api.v1 import controller
import escalator.installer.daisy.api as daisy_api

LOG = logging.getLogger(__name__)
_ = i18n._
_LE = i18n._LE
_LI = i18n._LI
_LW = i18n._LW
SUPPORTED_PARAMS = escalator.api.v1.SUPPORTED_PARAMS
SUPPORTED_FILTERS = escalator.api.v1.SUPPORTED_FILTERS
ACTIVE_IMMUTABLE = escalator.api.v1.ACTIVE_IMMUTABLE


# if some backends have order constraint, please add here
# if backend not in the next three order list, we will be
# think it does't have order constraint.
BACKENDS_INSTALL_ORDER = ['proton', 'zenic', 'tecs', 'kolla']
BACKENDS_UPGRADE_ORDER = ['proton', 'zenic', 'tecs', 'kolla']
BACKENDS_UNINSTALL_ORDER = []


class InstallTask(object):

    """
    Class for install OS and TECS.
    """
    """ Definition for install states."""

    def __init__(self, req, cluster_id, skip_pxe_ipmi):
        self.req = req
        self.cluster_id = cluster_id
        self.skip_pxe_ipmi = skip_pxe_ipmi


class Controller(controller.BaseController):

    """
    WSGI controller for hosts resource in Daisy v1 API

    The hosts resource API is a RESTful web service for host data. The API
    is as follows::

        GET  /hosts -- Returns a set of brief metadata about hosts
        GET  /hosts/detail -- Returns a set of detailed metadata about
                              hosts
        HEAD /hosts/<ID> -- Return metadata about an host with id <ID>
        GET  /hosts/<ID> -- Return host data for host with id <ID>
        POST /hosts -- Store host data and return metadata about the
                        newly-stored host
        PUT  /hosts/<ID> -- Update host metadata and/or upload host
                            data for a previously-reserved host
        DELETE /hosts/<ID> -- Delete the host with id <ID>
    """

    def __init__(self):
        self.notifier = notifier.Notifier()
        self.policy = policy.Enforcer()

    @utils.mutating
    def update_cluster(self, req, cluster_id, install_meta):
        """
        upgrade cluster.
        """
        self._enforce(req, 'update_cluster')
        try:
            status = daisy_api.update(req.context)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation=e.msg, request=req)
        return status


class InstallDeserializer(wsgi.JSONRequestDeserializer):
    """Handles deserialization of specific controller method requests."""

    def _deserialize(self, request):
        result = {}
        result["install_meta"] = utils.get_dict_meta(request)
        return result

    def update_cluster(self, request):
        return self._deserialize(request)


class InstallSerializer(wsgi.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def __init__(self):
        self.notifier = notifier.Notifier()

    def update_cluster(self, response, result):
        response.status = 201
        response.headers['Content-Type'] = 'application/json'
        response.body = self.to_json(result)
        return response


def create_resource():
    """Image members resource factory method"""
    deserializer = InstallDeserializer()
    serializer = InstallSerializer()
    return wsgi.Resource(Controller(), deserializer, serializer)
