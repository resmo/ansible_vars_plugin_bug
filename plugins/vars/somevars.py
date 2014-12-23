import socket
from ansible import errors

try:
    from netaddr import IPNetwork, IPAddress
except Exception, e:
    raise errors.AnsibleFilterError('python package missing run "pip install python-netaddr" on your workstation.')

class VarsModule(object):

    """
    Loads variables for groups and/or hosts
    """

    def __init__(self, inventory):

        """ constructor """

        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()


    def run(self, host, vault_password=None):
        """ For backwards compatibility, when only vars per host were retrieved
            This method should return both host specific vars as well as vars
            calculated from groups it is a member of """
        return {}


    def get_host_vars(self, host, vault_password=None):
        """ Get host specific variables. """

        result = {}

        inventory_hostname = host.get_variables()['inventory_hostname']
        ip = self._get_ip(inventory_hostname)

        if ip:
            result['ip'] = ip

        return result


    def get_group_vars(self, group, vault_password=None):
        """ Get group specific variables. """
        return {}


    def _get_zone(self, ip):
        for zone, networks in self._get_zones_defined().items():
            for network in networks:
                if IPAddress(ip) in IPNetwork(network):
                    return zone
        return ''


    def _get_ip(self, host):
        try:
            ip = socket.gethostbyname(host)
        except:
            ip = ''
        return ip

