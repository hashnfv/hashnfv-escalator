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

from __future__ import print_function

import copy
import functools
from oslo_utils import strutils
import escalatorclient.v1.versions
import escalatorclient.v1.clusters
import escalatorclient.v1.update
from escalatorclient.common import utils

_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


def _escalator_show(escalator, max_column_width=80):
    info = copy.deepcopy(escalator._info)
    exclusive_field = ('deleted', 'deleted_at')
    for field in exclusive_field:
        if field in info:
            info.pop(field)
    utils.print_dict(info, max_column_width=max_column_width)


@utils.arg('--type', metavar='<TYPE>',
           help='Type of escalator version, supported type are "internal": '
                'the internal version of escalator.')
def do_version(dc, args):
    """Get version of escalator."""
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    # Filter out values we can't use
    VERSION_PARAMS = escalatorclient.v1.versions.VERSION_PARAMS
    fields = dict(filter(lambda x: x[0] in VERSION_PARAMS, fields.items()))
    version = dc.versions.version(**fields)
    _escalator_show(version)


@utils.arg('--name', metavar='<NAME>',
           help='Filter version to those that have this name.')
@utils.arg('--status', metavar='<STATUS>',
           help='Filter version status.')
@utils.arg('--type', metavar='<type>',
           help='Filter by type.')
@utils.arg('--version', metavar='<version>',
           help='Filter by version number.')
@utils.arg('--page-size', metavar='<SIZE>', default=None, type=int,
           help='Number to request in each paginated request.')
@utils.arg('--sort-key', default='name',
           choices=escalatorclient.v1.versions.SORT_KEY_VALUES,
           help='Sort version list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=escalatorclient.v1.versions.SORT_DIR_VALUES,
           help='Sort version list in specified direction.')
def do_cluster_version_list(dc, args):
    """List hosts you can access."""
    filter_keys = ['name', 'type', 'status', 'version']
    filter_items = [(key, getattr(args, key)) for key in filter_keys]
    filters = dict([item for item in filter_items if item[1] is not None])

    kwargs = {'filters': filters}
    if args.page_size is not None:
        kwargs['page_size'] = args.page_size

    kwargs['sort_key'] = args.sort_key
    kwargs['sort_dir'] = args.sort_dir

    versions = dc.versions.list(**kwargs)

    columns = ['ID', 'NAME', 'TYPE', 'VERSION', 'size',
               'checksum', 'description', 'status', 'VERSION_PATCH']

    utils.print_list(versions, columns)


@utils.arg('--name', metavar='<NAME>',
           help='Filter version to those that have this name.')
@utils.arg('--status', metavar='<STATUS>',
           help='Filter version status.')
@utils.arg('--type', metavar='<type>',
           help='Filter by type.')
@utils.arg('--version', metavar='<version>',
           help='Filter by version number.')
@utils.arg('--page-size', metavar='<SIZE>', default=None, type=int,
           help='Number to request in each paginated request.')
@utils.arg('--sort-key', default='name',
           choices=escalatorclient.v1.versions.SORT_KEY_VALUES,
           help='Sort version list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=escalatorclient.v1.versions.SORT_DIR_VALUES,
           help='Sort version list in specified direction.')
def do_cluster_list(gc, args):
    """List clusters you can access."""
    filter_keys = ['name']
    filter_items = [(key, getattr(args, key)) for key in filter_keys]
    filters = dict([item for item in filter_items if item[1] is not None])

    kwargs = {'filters': filters}
    if args.page_size is not None:
        kwargs['page_size'] = args.page_size

    kwargs['sort_key'] = args.sort_key
    kwargs['sort_dir'] = args.sort_dir

    clusters = gc.clusters.list(**kwargs)

    columns = ['ID', 'Name', 'Description', 'Nodes', 'Networks',
               'Auto_scale', 'Use_dns', 'Status']
    utils.print_list(clusters, columns)


@utils.arg('id', metavar='<ID>',
           help='Filter cluster to those that have this id.')
def do_cluster_detail(gc, args):
    """List cluster you can access."""
    filter_keys = ['id']
    filter_items = [(key, getattr(args, key)) for key in filter_keys]
    filters = dict([item for item in filter_items if item[1] is not None])
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))
    kwargs = {'filters': filters}
    if filters:
        cluster = utils.find_resource(gc.clusters, fields.pop('id'))
        _escalator_show(cluster)
    else:
        cluster = gc.clusters.list(**kwargs)
        columns = ['ID', 'Name', 'Description', 'Nodes',
                   'Networks', 'Auto_scale', 'Use_dns']
        utils.print_list(cluster, columns)


@utils.arg('cluster_id', metavar='<CLUSTER_ID>',
           help='The cluster ID to update os and TECS.')
@utils.arg('--hosts', metavar='<HOSTS>', nargs='+',
           help='The host ID to update')
@utils.arg('--update-object', metavar='<UPDATE_OBJECT>',
           help='update object:vplat or tecs or zenic......')
@utils.arg('--version-id', metavar='<VERSION>',
           help='if not patch, update version id is used to update.')
@utils.arg('--version-patch-id', metavar='<VERSION_PATCH>',
           help='if update version patch, version patch id is needed')
@utils.arg('--update-script', metavar='<UPDATE_SCRIPT>',
           help='update script in /var/lib/daisy/os')
def do_update(gc, args):
    """update TECS."""
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    # Filter out values we can't use
    CREATE_PARAMS = escalatorclient.v1.update.CREATE_PARAMS
    fields = dict(filter(lambda x: x[0] in CREATE_PARAMS, fields.items()))

    update = gc.update.update(**fields)
    _escalator_show(update)
