Python API v1
=============

To create a client::

   from keystoneclient.auth.identity import v2 as identity
   from keystoneclient import session
   from escalatorclient import Client

   auth = identity.Password(auth_url=AUTH_URL,
                            username=USERNAME,
                            password=PASSWORD,
                            tenant_name=PROJECT_ID)

   sess = session.Session(auth=auth)
   token = auth.get_token(sess)

   escalator = Client('1', endpoint=OS_IMAGE_ENDPOINT, token=token)


List
----
List nodes you can access::

   for node in escalator.nodes.list():
      print node

