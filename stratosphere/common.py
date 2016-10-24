import re
from netaddr import IPNetwork

try:
    from stratosphere.utils import get_google_auth
except ImportError:
    # Python2
    from utils import get_google_auth


class ResourceValidators(object):
    @classmethod
    def regex_match(cls, regex, string):
        RE = re.compile(regex)
        if RE.match(string):
            return True
        return False

    @staticmethod
    def name(name):
        return ResourceValidators.regex_match('^(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)$', name)

    @staticmethod
    def zone(zone):
        return ResourceValidators.regex_match('^(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)$', zone)

    @staticmethod
    def base_instance_name(name):
        return ResourceValidators.regex_match('^[a-z][-a-z0-9]{0,57}$', name)

    @staticmethod
    def ipAddress(network):
        try:
            IPNetwork(network)
            return True
        except:
            raise ValueError('Invalid CIDR - {}'.format(network))

    @staticmethod
    def is_valid_machine_type(_type):
        return _type in [
            'n1-standard-1',
            'n1-standard-2',
            'n1-standard-4',
            'n1-standard-8',
            'n1-standard-16',
            'n1-standard-32',
            'n1-highmem-2',
            'n1-highmem-4',
            'n1-highmem-8',
            'n1-highmem-16',
            'n1-highmem-32',
            'n1-highcpu-2',
            'n1-highcpu-4',
            'n1-highcpu-8',
            'n1-highcpu-16',
            'n1-highcpu-32',
            'f1-micro',
            'g1-small',
        ]

    @staticmethod
    def is_url(value):
        if ResourceValidators.regex_match('^\$\(ref\..*.selfLink\)$', value):
            return True
        if ResourceValidators.regex_match('^http.*$', value):
            return True
        return False

class ResourceNames(object):
    """
    Provides some helper functions to consistently name things
    """
    def __init__(self, project, env):
        self.project = project
        self.env = env

    @property
    def networkName(self):
        return '{}-network'.format(self.env)

    @property
    def networkUrl(self):
        return "projects/{}/global/networks/{}".format(self.project, self.networkName)

    def subnetworkName(self, zone):
        return '{}-{}-subnetwork'.format(self.env, zone)

    def zone_to_region(self, zone):
        """Derives the region from a zone name."""
        parts = zone.split('-')
        if len(parts) != 3:
            raise Exception('Cannot derive region from zone "%s"' % zone)
        return '-'.join(parts[:2])
