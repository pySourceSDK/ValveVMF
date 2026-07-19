def VmfWrite(vmf, filename):

    vmf_text = vmf.vmf_str()

    # Must match the encoding VmfParse reads with, or material paths and
    # targetnames carrying non-ASCII bytes fail to round-trip.
    f = open(filename, "w", encoding="iso-8859-1")
    f.write(vmf_text)
    f.close()
