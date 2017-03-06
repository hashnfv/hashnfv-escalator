class BaseController(object):

    def get_cluster_meta_or_404(self, request, cluster_id):
        """
        Grabs the cluster metadata for an cluster with a supplied
        identifier or raises an HTTPNotFound (404) response

        :param request: The WSGI/Webob Request object
        :param cluster_id: The opaque cluster identifier

        :raises HTTPNotFound if cluster does not exist
        """
        pass
