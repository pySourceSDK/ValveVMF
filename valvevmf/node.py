from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from builtins import range
from builtins import object
from builtins import str
from future import standard_library
standard_library.install_aliases()

from valvevmf.property_writer import write_property  # NOQA: #402


class HoldsPropertiesAbstract(object):
    # def __init_props__(self, properties=None):
    def __init__(self, properties=None):
        """
        :param properties: The node's properties.
        :type properties: list[tuple], optional
        """

        if properties is None:
            properties = []

        #: :type: (list[tuple])
        self.properties = properties

    def __delitem__(self, attr):
        for i in range(len(self.properties)):
            if self.properties[i][0] == attr:
                del self.properties[i]
                return

    def __getitem__(self, attr):
        for i in range(len(self.properties)):
            if self.properties[i][0] == attr:
                return self.properties[i][1]
        return None

    def __setitem__(self, attr, value):
        for i in range(len(self.properties)):
            if self.properties[i][0] == attr:
                self.properties[i] = (attr, value)
                return

        self.properties.append((attr, value))

    def get_all(self, attr):
        """Every value stored under a property name.

        Property names are not unique: 'connections' repeats output names
        and 'allowed_verts' repeats keys, so indexing returns only the
        first. This returns all of them, in file order.

        :param attr: The property name to look up.
        :type attr: str
        :rtype: list
        """

        return [p[1] for p in self.properties if p[0] == attr]


class HoldsNodesAbstract(object):
    # def __init_nodes__(self, nodes=None):
    def __init__(self, nodes=None):
        """
        :param nodes: The node's sub-nodes
        :type nodes: list[VmfNode], optional
        """

        if nodes is None:
            nodes = []

        #: :type: (list[VmfNode], optional)
        self.nodes = nodes

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __delitem__(self, index):
        self.nodes.pop(index)

    def __getitem__(self, index):
        return self.nodes[index]

    def __setitem__(self, index, value):
        self.nodes[index] = value

    def children(self, name):
        """Every direct sub-node with a given name.

        :param name: The node name to match ('solid', 'side', 'entity'...).
        :type name: str
        :rtype: list[VmfNode]
        """

        return [n for n in self.nodes if n.name == name]


class VmfNode(HoldsPropertiesAbstract, HoldsNodesAbstract):
    def __init__(self, name, properties=None, nodes=None):
        """Creates an empty instance of VmfNode.

        :param name: indicates the node's type
        :type name: str
        """

        #: :type: (str) - The nodes's name ("world", "solid", "entity"...)
        self.name = name

        HoldsNodesAbstract.__init__(self, nodes)
        HoldsPropertiesAbstract.__init__(self, properties)

    def __delitem__(self, index):
        """Deletes the first instance of a property by name

        :param attr: The parameter name to delete
        :type attr: int, str
        """
        if isinstance(index, int):
            HoldsNodesAbstract.__delitem__(self, index)
        elif isinstance(index, str):
            HoldsPropertiesAbstract.__delitem__(self, index)
        else:
            raise LookupError

    def __getitem__(self, index):
        """Get the value for the first instance of a property by name

        :param attr: The parameter name to get.
        :type attr: str, int
        """
        if isinstance(index, int):
            return HoldsNodesAbstract.__getitem__(self, index)
        elif isinstance(index, str):
            return HoldsPropertiesAbstract.__getitem__(self, index)
        else:
            raise LookupError

    def __setitem__(self, index, value):
        """Sets the first instance of a property by name

        :param attr: The parameter name to set.
        :type attr: str
        :param value: The parameter value to use.
        :type attr: str
        """
        if isinstance(index, int):
            HoldsNodesAbstract.__setitem__(self, index, value)
        elif isinstance(index, str):
            HoldsPropertiesAbstract.__setitem__(self, index, value)
        else:
            raise LookupError

    def __repr__(self):
        """A partial, printable summary of a VmfNode.

        :returns: A Python formated string.
        :rtype: str
        """

        return '<VmfNode %(name)s %(p_len)x properties %(n_len)x subnodes>' % \
            {'name': self.name,
             'p_len': len(self.properties),
             'n_len': len(self.nodes)}

    def vmf_str(self, indent=0):
        vstr = '    ' * indent + self.name + '\n'
        vstr += '    ' * indent + '{\n'
        for p in self.properties:
            vstr += write_property(p, self.name, indent+1)
        for n in self.nodes:
            vstr += n.vmf_str(indent+1)
        vstr += '    ' * indent + '}\n'
        return vstr
