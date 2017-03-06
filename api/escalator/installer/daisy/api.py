from daisyclient.v1 import client as daisy_client


def daisyclient(request):
    DAISY_ENDPOINT_URL = "http://127.0.0.1:19292"
    return daisy_client.Client(version=1, endpoint=DAISY_ENDPOINT_URL)


def cluster_list(request):
    return daisyclient(request).clusters.list()


def cluster_get(request, cluster_id):
    return daisyclient(request).clusters.get(cluster_id)
