"""Round-trip fidelity: what goes in must come out.

The tests in writer.py compare vmf_str() against a file written from
vmf_str(), so they hold regardless of whether values survive. These
compare against the source instead.
"""
import os
import tempfile
import unittest
from decimal import Decimal

from valvevmf import Vmf, VmfNode


# Coordinates at TF2 map scale (playable space runs to +/-16384) with
# fractional parts, which is what Hammer writes for vertex-edited or
# rotated brushes. These are 7-9 significant digits.
PRECISE_VMF = '''world
{
\t"id" "1"
\t"classname" "worldspawn"
\tsolid
\t{
\t\t"id" "2"
\t\tside
\t\t{
\t\t\t"id" "3"
\t\t\t"plane" "(-12345.678 8192.375 -4096.0625) \
(12345.678 8192.375 -4096.0625) (12345.678 -8192.375 -4096.0625)"
\t\t\t"material" "DEV/DEV_MEASUREWALL01A"
\t\t\t"uaxis" "[1 0 0 -1234.5678] 0.25"
\t\t\t"vaxis" "[0 -1 0 8765.4321] 0.25"
\t\t\t"rotation" "0"
\t\t\t"lightmapscale" "16"
\t\t\t"smoothing_groups" "0"
\t\t}
\t}
}
'''


def _walk(node, path=''):
    here = path + '/' + node.name
    yield here, node
    for child in node.nodes:
        for item in _walk(child, here):
            yield item


def _flatten(nodes):
    out = []
    for root in nodes:
        for path, node in _walk(root):
            out.append((path, list(node.properties)))
    return out


class FidelityTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def _write(self, name, text, encoding='iso-8859-1'):
        path = os.path.join(self.test_dir, name)
        with open(path, 'w', encoding=encoding) as f:
            f.write(text)
        return path

    def testPrecisionSurvivesWrite(self):
        """Coordinates must not be rounded on save.

        Saving re-serializes the whole file, so a lossy number format
        moves geometry the caller never touched. At map scale the old
        '{:.6g}' format shifted -4096.0625 to -4096.06, which is enough
        to knock a face off-grid.
        """
        src = self._write('precise.vmf', PRECISE_VMF)
        out = os.path.join(self.test_dir, 'precise_out.vmf')
        Vmf(src).save(out)

        with open(out, encoding='iso-8859-1') as f:
            written = f.read()

        for value in ('-12345.678', '8192.375', '-4096.0625',
                      '-1234.5678', '8765.4321'):
            self.assertIn(value, written,
                          '{} was rounded away on save'.format(value))

    def testNoScientificNotation(self):
        """Hammer and VBSP read plain decimal literals only."""
        src = self._write('tiny.vmf', PRECISE_VMF.replace(
            '-1234.5678', '0.00000123'))
        out = os.path.join(self.test_dir, 'tiny_out.vmf')
        Vmf(src).save(out)

        with open(out, encoding='iso-8859-1') as f:
            written = f.read()

        self.assertNotIn('E+', written)
        self.assertNotIn('E-', written)
        self.assertIn('0.00000123', written)

    def testReparseIsStable(self):
        """Parsing our own output must yield an identical tree."""
        vmf = Vmf('tests/vmfs/testmap.vmf')
        out = os.path.join(self.test_dir, 'stable.vmf')
        vmf.save(out)

        before, after = _flatten(vmf.nodes), _flatten(Vmf(out).nodes)
        self.assertEqual(len(before), len(after))
        for (path_a, props_a), (path_b, props_b) in zip(before, after):
            self.assertEqual(path_a, path_b)
            self.assertEqual(props_a, props_b)

    def testNonAsciiSurvivesWrite(self):
        """The writer must use the encoding the parser reads with."""
        src = self._write('accents.vmf', PRECISE_VMF.replace(
            'DEV/DEV_MEASUREWALL01A', 'DEV/MUR_DÉCORÉ'))
        out = os.path.join(self.test_dir, 'accents_out.vmf')
        Vmf(src).save(out)

        with open(out, encoding='iso-8859-1') as f:
            self.assertIn('DEV/MUR_DÉCORÉ', f.read())

    def testScientificNotationInParsedField(self):
        """Hammer leaves sci-notation residue in uaxis/vaxis/plane/origin.

        Every spelling must read and survive a round trip: uppercase 'E'
        (Valve reference maps), explicit 'e+', and zero-padded exponents.
        These are real values pulled from the mapsrc corpus.
        """
        sci = PRECISE_VMF.replace(
            '"vaxis" "[0 -1 0 8765.4321] 0.25"',
            '"vaxis" "[-3.9733425E-8 -3.4549635E-10 -1.0 0] 0.25"')
        src = self._write('sci.vmf', sci)
        out = os.path.join(self.test_dir, 'sci_out.vmf')

        vmf = Vmf(src)
        side = vmf.nodes[0].nodes[0].nodes[0]
        # The axis vector parsed to Decimals, not a truncated '-3.9733425'.
        self.assertEqual(side['vaxis'][0], Decimal('-3.9733425E-8'))
        vmf.save(out)
        # And it re-parses identically, written as a plain decimal.
        again = Vmf(out).nodes[0].nodes[0].nodes[0]
        self.assertEqual(again['vaxis'][0], Decimal('-3.9733425E-8'))
        with open(out, encoding='iso-8859-1') as f:
            self.assertNotIn('E', f.read().split('vaxis')[1][:60])

    def testCameraLookRoundTrips(self):
        """'look' (Hammer camera nodes) is a bracketed vector on write.

        It parses via the global pp_vertex_arr into a bare tuple; the
        writer must restore the '[]' or the whole file fails to re-parse.
        Regression for the bug that corrupted every map with a saved
        editor camera.
        """
        cam_vmf = (
            'cameras\n{\n\t"activecamera" "-1"\n\tcamera\n\t{\n'
            '\t\t"position" "[0 0 0]"\n'
            '\t\t"look" "[104.201 -53.3603 199.605]"\n\t}\n}\n')
        src = self._write('cam.vmf', cam_vmf)
        out = os.path.join(self.test_dir, 'cam_out.vmf')
        Vmf(src).save(out)

        with open(out, encoding='iso-8859-1') as f:
            written = f.read()
        self.assertIn('"look" "[104.201 -53.3603 199.605]"', written)
        # The real proof: it re-parses without raising.
        again = Vmf(out)
        self.assertEqual(len(again.nodes), 1)


class NodeAccessTestCase(unittest.TestCase):
    def setUp(self):
        self.node = VmfNode(
            'side',
            properties=[('id', 3), ('material', 'DEV/DEV_MEASUREWALL01A')],
            nodes=[VmfNode('dispinfo')])

    def testGetPropertyReturnsValue(self):
        self.assertEqual(self.node['material'], 'DEV/DEV_MEASUREWALL01A')

    def testGetMissingPropertyIsNone(self):
        self.assertIsNone(self.node['nosuchkey'])

    def testSetExistingProperty(self):
        self.node['material'] = 'TOOLS/TOOLSNODRAW'
        self.assertEqual(self.node['material'], 'TOOLS/TOOLSNODRAW')
        self.assertEqual(len(self.node.properties), 2)

    def testSetNewProperty(self):
        self.node['rotation'] = 0
        self.assertEqual(self.node['rotation'], 0)
        self.assertEqual(len(self.node.properties), 3)

    def testDeleteProperty(self):
        del self.node['material']
        self.assertIsNone(self.node['material'])
        self.assertEqual(len(self.node.properties), 1)

    def testGetAllReturnsDuplicates(self):
        """'connections' repeats keys, so indexing alone loses values."""
        node = VmfNode('connections', properties=[
            ('OnMapSpawn', 'a,Kill,,0,-1'),
            ('OnMapSpawn', 'b,Kill,,0,-1')])
        self.assertEqual(len(node.get_all('OnMapSpawn')), 2)

    def testGetSubnodeByIndex(self):
        self.assertEqual(self.node[0].name, 'dispinfo')

    def testIterationYieldsSubnodes(self):
        self.assertEqual([n.name for n in self.node], ['dispinfo'])

    def testLenIsSubnodeCount(self):
        self.assertEqual(len(self.node), 1)

    def testChildrenFiltersByName(self):
        node = VmfNode('solid', nodes=[
            VmfNode('side'), VmfNode('side'), VmfNode('editor')])
        self.assertEqual(len(node.children('side')), 2)
        self.assertEqual(len(node.children('editor')), 1)


if __name__ == '__main__':
    unittest.main()
