import unittest
import os
import tempfile
import pyparsing
from valvevmf import *


class VmfParseTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.vmf_file = os.path.join(self.test_dir, 'testmap.vmf')

    def tearDown(self):
        return

    def testVmf(self):
        vmf = Vmf('tests/vmfs/testmap.vmf')
        self.assertEqual(61, len(vmf.nodes))

    def testMissingVmf(self):
        with self.assertRaises(Exception):
            vmf = Vmf('tests/vmfs/stairs002.vmf')

    def testSyntaxErrorVmf(self):
        f = open(self.vmf_file, "w")
        f.write("this file is obviously invalid")
        f.close()

        with self.assertRaises(pyparsing.ParseException):
            vmf = Vmf(self.vmf_file)
