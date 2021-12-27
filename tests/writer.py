import six
import os
import tempfile
import unittest
from valvevmf import *


class VmfWriteTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.vmf_file = os.path.join(self.test_dir, 'testmap.vmf')
        self.vmf = Vmf('tests/vmfs/testmap.vmf')
        self.vmf_temp = os.path.join(self.test_dir, 'test.vmf')
        return

    def tearDown(self):
        return

    def testWriteVmf(self):
        self.vmf.save(self.vmf_temp)
        with open(self.vmf_temp, 'r') as file:
            text_result = file.read()
        self.assertEqual(text_result, self.vmf.vmf_str())

    def testRepr(self):
        self.assertTrue(isinstance(repr(self.vmf), six.string_types))
