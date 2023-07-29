from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from valvevmf.node import HoldsNodesAbstract
from valvevmf.writer import VmfWrite
from valvevmf.parser import VmfParse
from builtins import object
from builtins import super
from future import standard_library
standard_library.install_aliases()


class Vmf(HoldsNodesAbstract):
    """
    This is the basic class to interact with vmf files, it is mostly a collection of VmfNodes.
    """

    def __init__(self, path=None):
        """
        initalize a Vmf file.

        :param path: The location of the vmf file to be parsed, saved as :any:`source_path<Vmf.source_path>`.
        :type path: str, optional
        """

        #: :type: (str) - The location of the parsed file
        self.source_path = path

        HoldsNodesAbstract.__init__(self, None)

        if self.source_path:
            self.nodes = VmfParse(self.source_path)

    def save(self, destination=None):
        """Saves the current instance of the Vmf. Overwrites original vmf file if no destination is provided.

        :param destination: A path (directory + filename) to determine where to save the vmf file.
        :type destination: str, optional
        """
        VmfWrite(self, destination or self.source_path)

    def vmf_str(self):
        vstr = ''
        for n in self.nodes:
            vstr += n.vmf_str()
        return vstr
