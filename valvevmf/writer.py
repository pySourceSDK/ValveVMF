from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()


def VmfWrite(vmf, filename):

    vmf_text = vmf.vmf_str()

    # Must match the encoding VmfParse reads with, or material paths and
    # targetnames carrying non-ASCII bytes fail to round-trip.
    f = open(filename, "w", encoding="iso-8859-1")
    f.write(vmf_text)
    f.close()
