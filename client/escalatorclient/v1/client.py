# Copyright 2012 OpenStack Foundation
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

from escalatorclient.common import http
from escalatorclient.common import utils
from escalatorclient.v1.versions import VersionManager
from escalatorclient.v1.clusters import ClusterManager
from escalatorclient.v1.update import UpdateManager


class Client(object):
    """Client for the escalator v1 API.

    :param string endpoint: A user-supplied endpoint URL for the escalator
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, endpoint, *args, **kwargs):
        """Initialize a new client for the escalator v1 API."""
        endpoint, version = utils.strip_version(endpoint)
        self.version = version or 1.0
        self.http_client = http.HTTPClient(endpoint, *args, **kwargs)
        self.versions = VersionManager(self.http_client)
        self.clusters = ClusterManager(self.http_client)
        self.update = UpdateManager(self.http_client)
