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
/clusters list for Escalator v1 API
"""
from oslo_log import log as logging
from webob.exc import HTTPBadRequest
from webob.exc import HTTPForbidden

from escalator.api import policy
from escalator.api.v1 import controller
from escalator.common import exception
from escalator.common import utils
from escalator.common import wsgi
from escalator import i18n
from escalator import notifier
import escalator.installer.daisy.api as daisy_api

LOG = logging.getLogger(__name__)
_ = i18n._
_LE = i18n._LE
_LI = i18n._LI
_LW = i18n._LW


class Controller(controller.BaseController):
    """
    WSGI controller for clusters resource in Escalaotr v1 API

    The clusters resource API is a RESTful web service for cluster data.
    The API is as follows::

        GET  /clusters -- Returns a set of brief metadata about clusters
        GET  /clusters -- Returns a set of detailed metadata about
                              clusters
    """
    def __init__(self):
        self.notifier = notifier.Notifier()
        self.policy = policy.Enforcer()

    def _enforce(self, req, action, target=None):
        """Authorize an action against our policies"""
        if target is None:
            target = {}
        try:
            self.policy.enforce(req.context, action, target)
        except exception.Forbidden:
            raise HTTPForbidden()

    def detail(self, req):
        """
        Returns detailed information for all available clusters

        :param req: The WSGI/Webob Request object
        :retval The response body is a mapping of the following form::

            {'clusters': [
                {'id': <ID>,
                 'name': <NAME>,
                 'nodes': <NODES>,
                 'networks': <NETWORKS>,
                 'description': <DESCRIPTION>,
                 'created_at': <TIMESTAMP>,
                 'updated_at': <TIMESTAMP>,
                 'deleted_at': <TIMESTAMP>|<NONE>,}, ...
            ]}
        """
        self._enforce(req, 'get_clusters')
        try:
            clusters = daisy_api.cluster_list(req.context)
            clusters_list = list()
            while True:
                try:
                    cluster_new = next(clusters)
                    clusters_list.append(cluster_new)
                except StopIteration:
                    break
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation=e.msg, request=req)
        return dict(clusters=clusters_list)


class ProjectDeserializer(wsgi.JSONRequestDeserializer):
    """Handles deserialization of specific controller method requests."""

    def _deserialize(self, request):
        result = {}
        result["cluster_meta"] = utils.get_cluster_meta(request)
        return result


class ProjectSerializer(wsgi.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def __init__(self):
        self.notifier = notifier.Notifier()

    def get_cluster(self, response, result):
        cluster_meta = result['cluster_meta']
        response.status = 201
        response.headers['Content-Type'] = 'application/json'
        response.body = self.to_json(dict(cluster=cluster_meta))
        return response


def create_resource():
    """Projects resource factory method"""
    deserializer = ProjectDeserializer()
    serializer = ProjectSerializer()
    return wsgi.Resource(Controller(), deserializer, serializer)
