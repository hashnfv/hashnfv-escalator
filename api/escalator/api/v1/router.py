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
from escalator.common import wsgi
from escalator.api.v1 import versions
from escalator.api.v1 import clusters
from escalator.api.v1 import install


class API(wsgi.Router):

    """WSGI router for Escalator v1 API requests."""

    def __init__(self, mapper):
        wsgi.Resource(wsgi.RejectMethodController())

        versions_resource = versions.create_resource()
        clusters_resource = clusters.create_resource()

        mapper.connect("/clusters",
                       controller=clusters_resource,
                       action='detail',
                       conditions={'method': ['GET']})

        mapper.connect("/versions",
                       controller=versions_resource,
                       action='version',
                       conditions={'method': ['POST']})

        install_resource = install.create_resource()
        mapper.connect("/update/{cluster_id}",
                       controller=install_resource,
                       action='update_progress',
                       conditions={'method': ['GET']})

        super(API, self).__init__(mapper)
