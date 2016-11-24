==============================
:program:`escalator` CLI man page
==============================

.. program:: escalator
.. highlight:: bash

SYNOPSIS
========

:program:`escalator` [options] <command> [command-options]

:program:`escalator help`

:program:`escalator help` <command>


DESCRIPTION
===========

The :program:`escalator` command line utility interacts with OpenStack Images
Service (escalator).

In order to use the CLI, you must provide your OpenStack username, password,
project (historically called tenant), and auth endpoint. You can use
configuration options :option:`--os-username`, :option:`--os-password`,
:option:`--os-tenant-id`, and :option:`--os-auth-url` or set corresponding
environment variables::

    export OS_USERNAME=user
    export OS_PASSWORD=pass
    export OS_TENANT_ID=b363706f891f48019483f8bd6503c54b
    export OS_AUTH_URL=http://auth.example.com:5000/v2.0

The command line tool will attempt to reauthenticate using provided
credentials for every request. You can override this behavior by manually
supplying an auth token using :option:`--os-image-url` and
:option:`--os-auth-token` or by setting corresponding environment variables::

    export OS_IMAGE_URL=http://escalator.example.org:9292/
    export OS_AUTH_TOKEN=3bcc3d3a03f44e3d8377f9247b0ad155


You can select an API version to use by :option:`--os-image-api-version`
option or by setting corresponding environment variable::

    export OS_IMAGE_API_VERSION=2

OPTIONS
=======

To get a list of available commands and options run::

    escalator help

To get usage and options of a command::

    escalator help <command>


EXAMPLES
========

Get information about image-create command::

    escalator help image-create

See available images::

    escalator image-list

Create new image::

    escalator image-create --name foo --disk-format=qcow2 \
                        --container-format=bare --is-public=True \
                        --copy-from http://somewhere.net/foo.img

Describe a specific image::

    escalator image-show foo


BUGS
====

escalator client is hosted in Launchpad so you can view current bugs at
https://bugs.launchpad.net/python-escalatorclient/.
