# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2014 SoftLayer Technologies, Inc.
# Copyright 2015 Mirantis, Inc
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
System-level utilities and helper functions.
"""

import errno
from functools import reduce

try:
    from eventlet import sleep
except ImportError:
    from time import sleep
from eventlet.green import socket

import functools
import os
import platform
import re
import subprocess
import sys
import uuid
import copy

from OpenSSL import crypto
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import encodeutils
from oslo_utils import excutils
import six
from webob import exc
from escalator.common import exception
from escalator import i18n

CONF = cfg.CONF

LOG = logging.getLogger(__name__)
_ = i18n._
_LE = i18n._LE


ESCALATOR_TEST_SOCKET_FD_STR = 'ESCALATOR_TEST_SOCKET_FD'


def chunkreadable(iter, chunk_size=65536):
    """
    Wrap a readable iterator with a reader yielding chunks of
    a preferred size, otherwise leave iterator unchanged.

    :param iter: an iter which may also be readable
    :param chunk_size: maximum size of chunk
    """
    return chunkiter(iter, chunk_size) if hasattr(iter, 'read') else iter


def chunkiter(fp, chunk_size=65536):
    """
    Return an iterator to a file-like obj which yields fixed size chunks

    :param fp: a file-like object
    :param chunk_size: maximum size of chunk
    """
    while True:
        chunk = fp.read(chunk_size)
        if chunk:
            yield chunk
        else:
            break


def cooperative_iter(iter):
    """
    Return an iterator which schedules after each
    iteration. This can prevent eventlet thread starvation.

    :param iter: an iterator to wrap
    """
    try:
        for chunk in iter:
            sleep(0)
            yield chunk
    except Exception as err:
        with excutils.save_and_reraise_exception():
            msg = _LE("Error: cooperative_iter exception %s") % err
            LOG.error(msg)


def cooperative_read(fd):
    """
    Wrap a file descriptor's read with a partial function which schedules
    after each read. This can prevent eventlet thread starvation.

    :param fd: a file descriptor to wrap
    """
    def readfn(*args):
        result = fd.read(*args)
        sleep(0)
        return result
    return readfn


MAX_COOP_READER_BUFFER_SIZE = 134217728  # 128M seems like a sane buffer limit


class CooperativeReader(object):

    """
    An eventlet thread friendly class for reading in image data.

    When accessing data either through the iterator or the read method
    we perform a sleep to allow a co-operative yield. When there is more than
    one image being uploaded/downloaded this prevents eventlet thread
    starvation, ie allows all threads to be scheduled periodically rather than
    having the same thread be continuously active.
    """

    def __init__(self, fd):
        """
        :param fd: Underlying image file object
        """
        self.fd = fd
        self.iterator = None
        # NOTE(markwash): if the underlying supports read(), overwrite the
        # default iterator-based implementation with cooperative_read which
        # is more straightforward
        if hasattr(fd, 'read'):
            self.read = cooperative_read(fd)
        else:
            self.iterator = None
            self.buffer = ''
            self.position = 0

    def read(self, length=None):
        """Return the requested amount of bytes, fetching the next chunk of
        the underlying iterator when needed.

        This is replaced with cooperative_read in __init__ if the underlying
        fd already supports read().
        """
        if length is None:
            if len(self.buffer) - self.position > 0:
                # if no length specified but some data exists in buffer,
                # return that data and clear the buffer
                result = self.buffer[self.position:]
                self.buffer = ''
                self.position = 0
                return str(result)
            else:
                # otherwise read the next chunk from the underlying iterator
                # and return it as a whole. Reset the buffer, as subsequent
                # calls may specify the length
                try:
                    if self.iterator is None:
                        self.iterator = self.__iter__()
                    return self.iterator.next()
                except StopIteration:
                    return ''
                finally:
                    self.buffer = ''
                    self.position = 0
        else:
            result = bytearray()
            while len(result) < length:
                if self.position < len(self.buffer):
                    to_read = length - len(result)
                    chunk = self.buffer[self.position:self.position + to_read]
                    result.extend(chunk)

                    # This check is here to prevent potential OOM issues if
                    # this code is called with unreasonably high values of read
                    # size. Currently it is only called from the HTTP clients
                    # of Glance backend stores, which use httplib for data
                    # streaming, which has readsize hardcoded to 8K, so this
                    # check should never fire. Regardless it still worths to
                    # make the check, as the code may be reused somewhere else.
                    if len(result) >= MAX_COOP_READER_BUFFER_SIZE:
                        raise exception.LimitExceeded()
                    self.position += len(chunk)
                else:
                    try:
                        if self.iterator is None:
                            self.iterator = self.__iter__()
                        self.buffer = self.iterator.next()
                        self.position = 0
                    except StopIteration:
                        self.buffer = ''
                        self.position = 0
                        return str(result)
            return str(result)

    def __iter__(self):
        return cooperative_iter(self.fd.__iter__())


class LimitingReader(object):

    """
    Reader designed to fail when reading image data past the configured
    allowable amount.
    """

    def __init__(self, data, limit):
        """
        :param data: Underlying image data object
        :param limit: maximum number of bytes the reader should allow
        """
        self.data = data
        self.limit = limit
        self.bytes_read = 0

    def __iter__(self):
        for chunk in self.data:
            self.bytes_read += len(chunk)
            if self.bytes_read > self.limit:
                raise exception.ImageSizeLimitExceeded()
            else:
                yield chunk

    def read(self, i):
        result = self.data.read(i)
        self.bytes_read += len(result)
        if self.bytes_read > self.limit:
            raise exception.ImageSizeLimitExceeded()
        return result


def get_dict_meta(response):
    result = {}
    for key, value in response.json.items():
        result[key] = value
    return result


def create_mashup_dict(image_meta):
    """
    Returns a dictionary-like mashup of the image core properties
    and the image custom properties from given image metadata.

    :param image_meta: metadata of image with core and custom properties
    """

    def get_items():
        for key, value in six.iteritems(image_meta):
            if isinstance(value, dict):
                for subkey, subvalue in six.iteritems(
                        create_mashup_dict(value)):
                    if subkey not in image_meta:
                        yield subkey, subvalue
            else:
                yield key, value

    return dict(get_items())


def safe_mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def safe_remove(path):
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


class PrettyTable(object):

    """Creates an ASCII art table for use in bin/escalator

    """

    def __init__(self):
        self.columns = []

    def add_column(self, width, label="", just='l'):
        """Add a column to the table

        :param width: number of characters wide the column should be
        :param label: column heading
        :param just: justification for the column, 'l' for left,
                     'r' for right
        """
        self.columns.append((width, label, just))

    def make_header(self):
        label_parts = []
        break_parts = []
        for width, label, _ in self.columns:
            # NOTE(sirp): headers are always left justified
            label_part = self._clip_and_justify(label, width, 'l')
            label_parts.append(label_part)

            break_part = '-' * width
            break_parts.append(break_part)

        label_line = ' '.join(label_parts)
        break_line = ' '.join(break_parts)
        return '\n'.join([label_line, break_line])

    def make_row(self, *args):
        row = args
        row_parts = []
        for data, (width, _, just) in zip(row, self.columns):
            row_part = self._clip_and_justify(data, width, just)
            row_parts.append(row_part)

        row_line = ' '.join(row_parts)
        return row_line

    @staticmethod
    def _clip_and_justify(data, width, just):
        # clip field to column width
        clipped_data = str(data)[:width]

        if just == 'r':
            # right justify
            justified = clipped_data.rjust(width)
        else:
            # left justify
            justified = clipped_data.ljust(width)

        return justified


def get_terminal_size():

    def _get_terminal_size_posix():
        import fcntl
        import struct
        import termios

        height_width = None

        try:
            height_width = struct.unpack('hh', fcntl.ioctl(sys.stderr.fileno(),
                                                           termios.TIOCGWINSZ,
                                                           struct.pack(
                                                               'HH', 0, 0)))
        except Exception:
            pass

        if not height_width:
            try:
                p = subprocess.Popen(['stty', 'size'],
                                     shell=False,
                                     stdout=subprocess.PIPE,
                                     stderr=open(os.devnull, 'w'))
                result = p.communicate()
                if p.returncode == 0:
                    return tuple(int(x) for x in result[0].split())
            except Exception:
                pass

        return height_width

    def _get_terminal_size_win32():
        try:
            from ctypes import create_string_buffer
            from ctypes import windll
            handle = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        except Exception:
            return None
        if res:
            import struct
            unpack_tmp = struct.unpack("hhhhHhhhhhh", csbi.raw)
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom, maxx, maxy) = unpack_tmp
            height = bottom - top + 1
            width = right - left + 1
            return (height, width)
        else:
            return None

    def _get_terminal_size_unknownOS():
        raise NotImplementedError

    func = {'posix': _get_terminal_size_posix,
            'win32': _get_terminal_size_win32}

    height_width = func.get(platform.os.name, _get_terminal_size_unknownOS)()

    if height_width is None:
        raise exception.Invalid()

    for i in height_width:
        if not isinstance(i, int) or i <= 0:
            raise exception.Invalid()

    return height_width[0], height_width[1]


def mutating(func):
    """Decorator to enforce read-only logic"""
    @functools.wraps(func)
    def wrapped(self, req, *args, **kwargs):
        if req.context.read_only:
            msg = "Read-only access"
            LOG.debug(msg)
            raise exc.HTTPForbidden(msg, request=req,
                                    content_type="text/plain")
        return func(self, req, *args, **kwargs)
    return wrapped


def setup_remote_pydev_debug(host, port):
    error_msg = _LE('Error setting up the debug environment. Verify that the'
                    ' option pydev_worker_debug_host is pointing to a valid '
                    'hostname or IP on which a pydev server is listening on'
                    ' the port indicated by pydev_worker_debug_port.')

    try:
        try:
            from pydev import pydevd
        except ImportError:
            import pydevd

        pydevd.settrace(host,
                        port=port,
                        stdoutToServer=True,
                        stderrToServer=True)
        return True
    except Exception:
        with excutils.save_and_reraise_exception():
            LOG.exception(error_msg)


def validate_key_cert(key_file, cert_file):
    try:
        error_key_name = "private key"
        error_filename = key_file
        with open(key_file, 'r') as keyfile:
            key_str = keyfile.read()
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_str)

        error_key_name = "certificate"
        error_filename = cert_file
        with open(cert_file, 'r') as certfile:
            cert_str = certfile.read()
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_str)
    except IOError as ioe:
        raise RuntimeError(_("There is a problem with your %(error_key_name)s "
                             "%(error_filename)s.  Please verify it."
                             "  Error: %(ioe)s") %
                           {'error_key_name': error_key_name,
                            'error_filename': error_filename,
                            'ioe': ioe})
    except crypto.Error as ce:
        raise RuntimeError(_("There is a problem with your %(error_key_name)s "
                             "%(error_filename)s.  Please verify it. OpenSSL"
                             " error: %(ce)s") %
                           {'error_key_name': error_key_name,
                            'error_filename': error_filename,
                            'ce': ce})

    try:
        data = str(uuid.uuid4())
        digest = CONF.digest_algorithm
        if digest == 'sha1':
            LOG.warn('The FIPS (FEDERAL INFORMATION PROCESSING STANDARDS)'
                     ' state that the SHA-1 is not suitable for'
                     ' general-purpose digital signature applications (as'
                     ' specified in FIPS 186-3) that require 112 bits of'
                     ' security. The default value is sha1 in Kilo for a'
                     ' smooth upgrade process, and it will be updated'
                     ' with sha256 in next release(L).')
        out = crypto.sign(key, data, digest)
        crypto.verify(cert, out, data, digest)
    except crypto.Error as ce:
        raise RuntimeError(_("There is a problem with your key pair.  "
                             "Please verify that cert %(cert_file)s and "
                             "key %(key_file)s belong together.  OpenSSL "
                             "error %(ce)s") % {'cert_file': cert_file,
                                                'key_file': key_file,
                                                'ce': ce})


def get_test_suite_socket():
    global ESCALATOR_TEST_SOCKET_FD_STR
    if ESCALATOR_TEST_SOCKET_FD_STR in os.environ:
        fd = int(os.environ[ESCALATOR_TEST_SOCKET_FD_STR])
        sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        sock = socket.SocketType(_sock=sock)
        sock.listen(CONF.backlog)
        del os.environ[ESCALATOR_TEST_SOCKET_FD_STR]
        os.close(fd)
        return sock
    return None


def is_uuid_like(val):
    """Returns validation of a value as a UUID.

    For our purposes, a UUID is a canonical form string:
    aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
    """
    try:
        return str(uuid.UUID(val)) == val
    except (TypeError, ValueError, AttributeError):
        return False


def exception_to_str(exc):
    try:
        error = six.text_type(exc)
    except UnicodeError:
        try:
            error = str(exc)
        except UnicodeError:
            error = ("Caught '%(exception)s' exception." %
                     {"exception": exc.__class__.__name__})
    return encodeutils.safe_encode(error, errors='ignore')


try:
    REGEX_4BYTE_UNICODE = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
    # UCS-2 build case
    REGEX_4BYTE_UNICODE = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')


def no_4byte_params(f):
    """
    Checks that no 4 byte unicode characters are allowed
    in dicts' keys/values and string's parameters
    """
    def wrapper(*args, **kwargs):

        def _is_match(some_str):
            return (isinstance(some_str, unicode) and
                    REGEX_4BYTE_UNICODE.findall(some_str) != [])

        def _check_dict(data_dict):
            # a dict of dicts has to be checked recursively
            for key, value in data_dict.iteritems():
                if isinstance(value, dict):
                    _check_dict(value)
                else:
                    if _is_match(key):
                        msg = _("Property names can't contain 4 byte unicode.")
                        raise exception.Invalid(msg)
                    if _is_match(value):
                        msg = (_("%s can't contain 4 byte unicode characters.")
                               % key.title())
                        raise exception.Invalid(msg)

        for data_dict in [arg for arg in args if isinstance(arg, dict)]:
            _check_dict(data_dict)
        # now check args for str values
        for arg in args:
            if _is_match(arg):
                msg = _("Param values can't contain 4 byte unicode.")
                raise exception.Invalid(msg)
        # check kwargs as well, as params are passed as kwargs via
        # registry calls
        _check_dict(kwargs)
        return f(*args, **kwargs)
    return wrapper


def stash_conf_values():
    """
    Make a copy of some of the current global CONF's settings.
    Allows determining if any of these values have changed
    when the config is reloaded.
    """
    conf = {}
    conf['bind_host'] = CONF.bind_host
    conf['bind_port'] = CONF.bind_port
    conf['tcp_keepidle'] = CONF.cert_file
    conf['backlog'] = CONF.backlog
    conf['key_file'] = CONF.key_file
    conf['cert_file'] = CONF.cert_file

    return conf


def validate_ip_format(ip_str):
    '''
    valid ip_str format = '10.43.178.9'
    invalid ip_str format : '123. 233.42.12', spaces existed in field
                            '3234.23.453.353', out of range
                            '-2.23.24.234', negative number in field
                            '1.2.3.4d', letter in field
                            '10.43.1789', invalid format
    '''
    if not ip_str:
        msg = (_("No ip given when check ip"))
        LOG.error(msg)
        raise exc.HTTPBadRequest(msg, content_type="text/plain")

    valid_fromat = False
    if ip_str.count('.') == 3 and all(num.isdigit() and 0 <= int(
            num) < 256 for num in ip_str.rstrip().split('.')):
        valid_fromat = True
    if not valid_fromat:
        msg = (_("%s invalid ip format!") % ip_str)
        LOG.error(msg)
        raise exc.HTTPBadRequest(msg, content_type="text/plain")


def valid_cidr(cidr):
    if not cidr:
        msg = (_("No CIDR given."))
        LOG.error(msg)
        raise exc.HTTPBadRequest(explanation=msg)

    cidr_division = cidr.split('/')
    if (len(cidr_division) != 2 or
            not cidr_division[0] or
            not cidr_division[1]):
        msg = (_("CIDR format error."))
        LOG.error(msg)
        raise exc.HTTPBadRequest(explanation=msg)

    netmask_err_msg = (_("CIDR netmask error, "
                         "it should be a integer between 0-32."))
    try:
        netmask_cidr = int(cidr_division[1])
    except ValueError:
        LOG.warn(netmask_err_msg)
        raise exc.HTTPBadRequest(explanation=netmask_err_msg)

    if (netmask_cidr < 0 and
            netmask_cidr > 32):
        LOG.warn(netmask_err_msg)
        raise exc.HTTPBadRequest(explanation=netmask_err_msg)

    validate_ip_format(cidr_division[0])


def ip_into_int(ip):
    """
    Switch ip string to decimalism integer..
    :param ip: ip string
    :return: decimalism integer
    """
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


def int_into_ip(num):
    s = []
    for i in range(4):
        s.append(str(num % 256))
        num /= 256
    return '.'.join(s[::-1])


def is_ip_in_cidr(ip, cidr):
    """
    Check ip is in cidr
    :param ip: Ip will be checked, like:192.168.1.2.
    :param cidr: Ip range,like:192.168.0.0/24.
    :return: If ip in cidr, return True, else return False.
    """
    if not ip:
        msg = "Error, ip is empty"
        raise exc.HTTPBadRequest(explanation=msg)
    if not cidr:
        msg = "Error, CIDR is empty"
        raise exc.HTTPBadRequest(explanation=msg)
    network = cidr.split('/')
    mask = ~(2**(32 - int(network[1])) - 1)
    return (ip_into_int(ip) & mask) == (ip_into_int(network[0]) & mask)


def is_ip_in_ranges(ip, ip_ranges):
    """
    Check ip is in range
    : ip: Ip will be checked, like:192.168.1.2.
    : ip_ranges : Ip ranges, like:
                    [{'start':'192.168.0.10', 'end':'192.168.0.20'}
                    {'start':'192.168.0.50', 'end':'192.168.0.60'}]
    :return: If ip in ip_ranges, return True, else return False.
    """
    if not ip:
        msg = "Error, ip is empty"
        raise exc.HTTPBadRequest(explanation=msg)

    if not ip_ranges:
        return True

    for ip_range in ip_ranges:
        start_ip_int = ip_into_int(ip_range['start'])
        end_ip_int = ip_into_int(ip_range['end'])
        ip_int = ip_into_int(ip)
        if ip_int >= start_ip_int and ip_int <= end_ip_int:
            return True

    return False


def merge_ip_ranges(ip_ranges):
    if not ip_ranges:
        return ip_ranges
    sort_ranges_by_start_ip = {}
    for ip_range in ip_ranges:
        start_ip_int = ip_into_int(ip_range['start'])
        sort_ranges_by_start_ip.update({str(start_ip_int): ip_range})
    sort_ranges = [sort_ranges_by_start_ip[key] for key in
                   sorted(sort_ranges_by_start_ip.keys())]
    last_range_end_ip = None

    merged_ip_ranges = []
    for ip_range in sort_ranges:
        if last_range_end_ip is None:
            last_range_end_ip = ip_range['end']
            merged_ip_ranges.append(ip_range)
            continue
        else:
            last_range_end_ip_int = ip_into_int(last_range_end_ip)
            ip_range_start_ip_int = ip_into_int(ip_range['start'])
            if (last_range_end_ip_int + 1) == ip_range_start_ip_int:
                merged_ip_ranges[-1]['end'] = ip_range['end']
            else:
                merged_ip_ranges.append(ip_range)
    return merged_ip_ranges


def _split_ip_ranges(ip_ranges):
    ip_ranges_start = set()
    ip_ranges_end = set()
    if not ip_ranges:
        return (ip_ranges_start, ip_ranges_end)

    for ip_range in ip_ranges:
        ip_ranges_start.add(ip_range['start'])
        ip_ranges_end.add(ip_range['end'])

    return (ip_ranges_start, ip_ranges_end)


# [{'start':'192.168.0.10', 'end':'192.168.0.20'},
#  {'start':'192.168.0.21', 'end':'192.168.0.22'}] and
# [{'start':'192.168.0.10', 'end':'192.168.0.22'}] is equal here
def is_ip_ranges_equal(ip_ranges1, ip_ranges2):
    if not ip_ranges1 and not ip_ranges2:
        return True
    if ((ip_ranges1 and not ip_ranges2) or
            (ip_ranges2 and not ip_ranges1)):
        return False
    ip_ranges_1 = copy.deepcopy(ip_ranges1)
    ip_ranges_2 = copy.deepcopy(ip_ranges2)
    merged_ip_ranges1 = merge_ip_ranges(ip_ranges_1)
    merged_ip_ranges2 = merge_ip_ranges(ip_ranges_2)
    ip_ranges1_start, ip_ranges1_end = _split_ip_ranges(merged_ip_ranges1)
    ip_ranges2_start, ip_ranges2_end = _split_ip_ranges(merged_ip_ranges2)
    if (ip_ranges1_start == ip_ranges2_start and
            ip_ranges1_end == ip_ranges2_end):
        return True
    else:
        return False


def get_dvs_interfaces(host_interfaces):
    dvs_interfaces = []
    if not isinstance(host_interfaces, list):
        host_interfaces = eval(host_interfaces)
    for interface in host_interfaces:
        if not isinstance(interface, dict):
            interface = eval(interface)
        if ('vswitch_type' in interface and
                interface['vswitch_type'] == 'dvs'):
            dvs_interfaces.append(interface)

    return dvs_interfaces


def get_clc_pci_info(pci_info):
    clc_pci = []
    flag1 = 'Intel Corporation Coleto Creek PCIe Endpoint'
    flag2 = '8086:0435'
    for pci in pci_info:
        if flag1 in pci or flag2 in pci:
            clc_pci.append(pci.split()[0])
    return clc_pci


def cpu_str_to_list(spec):
    """Parse a CPU set specification.

    :param spec: cpu set string eg "1-4,^3,6"

    Each element in the list is either a single
    CPU number, a range of CPU numbers, or a
    caret followed by a CPU number to be excluded
    from a previous range.

    :returns: a set of CPU indexes
    """

    cpusets = []
    if not spec:
        return cpusets

    cpuset_ids = set()
    cpuset_reject_ids = set()
    for rule in spec.split(','):
        rule = rule.strip()
        # Handle multi ','
        if len(rule) < 1:
            continue
        # Note the count limit in the .split() call
        range_parts = rule.split('-', 1)
        if len(range_parts) > 1:
            # So, this was a range; start by converting the parts to ints
            try:
                start, end = [int(p.strip()) for p in range_parts]
            except ValueError:
                raise exception.Invalid(_("Invalid range expression %r")
                                        % rule)
            # Make sure it's a valid range
            if start > end:
                raise exception.Invalid(_("Invalid range expression %r")
                                        % rule)
            # Add available CPU ids to set
            cpuset_ids |= set(range(start, end + 1))
        elif rule[0] == '^':
            # Not a range, the rule is an exclusion rule; convert to int
            try:
                cpuset_reject_ids.add(int(rule[1:].strip()))
            except ValueError:
                raise exception.Invalid(_("Invalid exclusion "
                                          "expression %r") % rule)
        else:
            # OK, a single CPU to include; convert to int
            try:
                cpuset_ids.add(int(rule))
            except ValueError:
                raise exception.Invalid(_("Invalid inclusion "
                                          "expression %r") % rule)

    # Use sets to handle the exclusion rules for us
    cpuset_ids -= cpuset_reject_ids
    cpusets = list(cpuset_ids)
    cpusets.sort()
    return cpusets


def cpu_list_to_str(cpu_list):
    """Parse a CPU list to string.

    :param cpu_list: eg "[1,2,3,4,6,7]"

    :returns: a string of CPU ranges, eg 1-4,6,7
    """
    spec = ''
    if not cpu_list:
        return spec

    cpu_list.sort()
    count = 0
    group_cpus = []
    tmp_cpus = []
    for cpu in cpu_list:
        if count == 0:
            init = cpu
            tmp_cpus.append(cpu)
        else:
            if cpu == (init + count):
                tmp_cpus.append(cpu)
            else:
                group_cpus.append(tmp_cpus)
                tmp_cpus = []
                count = 0
                init = cpu
                tmp_cpus.append(cpu)
        count += 1

    group_cpus.append(tmp_cpus)

    for group in group_cpus:
        if len(group) > 2:
            group_spec = ("%s-%s" % (group[0], group[0]+len(group)-1))
        else:
            group_str = [str(num) for num in group]
            group_spec = ','.join(group_str)
        if spec:
            spec += ',' + group_spec
        else:
            spec = group_spec

    return spec


def simple_subprocess_call(cmd):
    return_code = subprocess.call(cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    return return_code


def translate_quotation_marks_for_shell(orig_str):
    translated_str = ''
    quotation_marks = '"'
    quotation_marks_count = orig_str.count(quotation_marks)
    if quotation_marks_count > 0:
        replace_marks = '\\"'
        translated_str = orig_str.replace(quotation_marks, replace_marks)
    else:
        translated_str = orig_str
    return translated_str


def translate_marks_4_sed_command(ori_str):
    translated_str = ori_str
    translated_marks = {
        '/': '\/',
        '.': '\.',
        '"': '\\"'}
    for translated_mark in translated_marks:
        if translated_str.count(translated_mark):
            translated_str = translated_str.\
                replace(translated_mark, translated_marks[translated_mark])
    return translated_str
