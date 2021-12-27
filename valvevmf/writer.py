from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()


def VmfWrite(vmf, filename):

    vmf_text = vmf.vmf_str()

    f = open(filename, "w")
    f.write(vmf_text)
    f.close()
