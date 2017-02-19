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
from oslo_utils import encodeutils
from oslo_utils import strutils
import escalatorclient.v1.versions
from escalatorclient.common import utils
from escalatorclient import exc

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
    VERSION_PARAMS = escalatorclient.v1.version.VERSION_PARAMS
    fields = dict(filter(lambda x: x[0] in VERSION_PARAMS, fields.items()))
    version = dc.version.version(**fields)
    _escalator_show(version)


@utils.arg('id', metavar='<ID>',
           help='Filter version to those that have this id.')
def do_version_detail(dc, args):
    """Get backend_types of escalator."""
    version = utils.find_resource(dc.versions, args.id)
    _escalator_show(version)


@utils.arg('name', metavar='<NAME>',
           help='name of version.')
@utils.arg('type', metavar='<TYPE>',
           help='version type.eg redhat7.0...')
@utils.arg('--size', metavar='<SIZE>',
           help='size of the version file.')
@utils.arg('--checksum', metavar='<CHECKSUM>',
           help='md5 of version file')
@utils.arg('--version', metavar='<VERSION>',
           help='version number of version file')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='description of version file')
@utils.arg('--status', metavar='<STATUS>',
           help='version file status.default:init')
def do_version_add(dc, args):
    """Add a version."""

    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    # Filter out values we can't use
    CREATE_PARAMS = escalatorclient.v1.versions.CREATE_PARAMS
    fields = dict(filter(lambda x: x[0] in CREATE_PARAMS, fields.items()))

    version = dc.versions.add(**fields)
    _escalator_show(version)


@utils.arg('id', metavar='<ID>',
           help='ID of versions.')
@utils.arg('--name', metavar='<NAME>',
           help='name of version.')
@utils.arg('--type', metavar='<TYPE>',
           help='version type.eg redhat7.0...')
@utils.arg('--size', metavar='<SIZE>',
           help='size of the version file.')
@utils.arg('--checksum', metavar='<CHECKSUM>',
           help='md5 of version file')
@utils.arg('--version', metavar='<VERSION>',
           help='version number of version file')
@utils.arg('--description', metavar='<DESCRIPTION>',
           help='description of version file')
@utils.arg('--status', metavar='<STATUS>',
           help='version file status.default:init')
def do_version_update(dc, args):
    """Add a version."""

    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))

    # Filter out values we can't use
    CREATE_PARAMS = escalatorclient.v1.versions.CREATE_PARAMS
    fields = dict(filter(lambda x: x[0] in CREATE_PARAMS, fields.items()))
    version_id = fields.get('id', None)
    version = dc.versions.update(version_id, **fields)
    _escalator_show(version)


@utils.arg('id', metavar='<ID>', nargs='+',
           help='ID of versions.')
def do_version_delete(dc, args):
    """Delete specified template(s)."""
    fields = dict(filter(lambda x: x[1] is not None, vars(args).items()))
    versions = fields.get('id', None)
    for version in versions:
        try:
            if args.verbose:
                print('Requesting version delete for %s ...' %
                      encodeutils.safe_decode(version), end=' ')
            dc.versions.delete(version)
            if args.verbose:
                print('[Done]')
        except exc.HTTPException as e:
            if args.verbose:
                print('[Fail]')
            print('%s: Unable to delete version %s' % (e, version))


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


@utils.arg('id', metavar='<ID>',
           help='Filter version patch to those that have this id.')
def do_version_patch_detail(dc, args):
    """Get version_patch of escalator."""
    version = utils.find_resource(dc.version_patchs, args.id)
    _escalator_show(version)
