from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object

from valvevmf.property_writer import write_property


class VmfNode(object):
    def __init__(self, name, properties=None, nodes=None):

        if properties is None:
            properties = []

        if nodes is None:
            nodes = []

        self.name = name
        self.properties = properties
        self.nodes = nodes

    def vmf_str(self, indent=0):
        vstr = '    ' * indent + self.name + '\n'
        vstr += '    ' * indent + '{\n'
        for p in self.properties:
            vstr += write_property(p, self.name, indent+1)
        for n in self.nodes:
            vstr += n.vmf_str(indent+1)
        vstr += '     ' * indent + '}\n'
        return vstr

    def __repr__(self):
        """A partial, printable summary of a VmfNode.

        :returns: A Python formated string.
        :rtype: str
        """

        return '<VmfNode %(name)s %(p_len)x %(n_len)x' % \
            {'name': self.name,
             'p_len': len(self.properties),
             'n_len': len(self.nodes)}
