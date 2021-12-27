from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object


class VMFNode(object):
    def __init__(self, name, properties=None, nodes=None):

        if properties is None:
            properties = []

        if nodes is None:
            nodes = []

        self.name = name
        self.properties = properties
        self.nodes = nodes

    def vmf_str(self, indent=0):
        vstr = '\t' * indent + self.name + '\n'
        vstr += '\t' * indent + '{\n'
        for p in self.properties:
            vstr += '\t' * (indent+1) + str(p) + '\n'
        for n in self.nodes:
            vstr += n.vmf_str(indent+1)
        vstr += '\t' * indent + '}\n'
        return vstr

    def __repr__(self):
        """A partial, printable summary of a VMFNode.

        :returns: A Python formated string.
        :rtype: str
        """

        return "<VMFNode " + str(self.name) + ">"
