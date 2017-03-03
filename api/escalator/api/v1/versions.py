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
/hosts endpoint for Escalator v1 API
"""
from oslo_log import log as logging
from escalator import i18n
from escalator import notifier
from escalator.common import utils
from escalator.common import wsgi
from escalator.version import version_info


LOG = logging.getLogger(__name__)
_ = i18n._
_LE = i18n._LE
_LI = i18n._LI
_LW = i18n._LW


class Controller():
    """
    WSGI controller for hosts resource in Escalator v1 API

    """
    def __init__(self):
        self.notifier = notifier.Notifier()

    @utils.mutating
    def version(self, req, version):
        """
        Get version of esclator.
        :param req: The WSGI/Webob Request object
        """
        if version.get('type') == 'pbr':
            return {"escalator_version":
                    version_info.version_string_with_vcs()}
        else:
            # reserved for external version
            return {"escalator_version": '1.0.0-1.1.0'}


class VersionDeserializer(wsgi.JSONRequestDeserializer):
    """Handles deserialization of specific controller method requests."""

    def _deserialize(self, request):
        result = {}
        result['file_meta'] = utils.get_dict_meta(request)
        return result

    def version(self, request):
        result = {}
        result['version'] = utils.get_dict_meta(request)
        return result


class VersionSerializer(wsgi.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def __init__(self):
        self.notifier = notifier.Notifier()

    def version(self, response, result):
        response.status = 201
        response.headers['Content-Type'] = 'application/json'
        response.body = self.to_json(result)
        return response


def create_resource():
    """Version resource factory method"""
    deserializer = VersionDeserializer()
    serializer = VersionSerializer()
    return wsgi.Resource(Controller(), deserializer, serializer)
