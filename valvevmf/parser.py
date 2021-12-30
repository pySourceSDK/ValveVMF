from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from builtins import map
from builtins import str
from builtins import range
from builtins import dict
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()

from collections import namedtuple

import os  # NOQA: E402
from pyparsing import *  # NOQA: E402

from valvevmf.vmf import *  # NOQA: E402
from valvevmf.node import VmfNode  # NOQA: E402

from valvevmf.property_parser import parse_property, pp_float, pp_uint8, pp_vertex_content


def asTuple(data):
    return [tuple(data.asList()[0])]


def asList(data):
    return list(data.asList())


def asGrid(data):
    return ('rows', [d for d in data])


# Node parsing
pp_vnode = Forward()
pp_node_name = Word(alphas+'_')
pp_node_keyval = Group(QuotedString('"') + QuotedString('"'))
pp_node_keyval.setParseAction(asTuple)

pp_gridnode_float_name = Literal('distances') ^ Literal('alphas')
pp_gridnode_float_cont = Suppress('{') + ZeroOrMore(
    Suppress(QuotedString('"')) + Suppress('"') +
    Group(ZeroOrMore(pp_float)).setParseAction(asList) +
    Suppress('"')).setParseAction(asGrid) + Suppress('}')

pp_gridnode_uint8_name = Literal('triangle_tags')
pp_gridnode_uint8_cont = Suppress('{') + ZeroOrMore(
    Suppress(QuotedString('"')) + Suppress('"') +
    Group(ZeroOrMore(pp_uint8)).setParseAction(asList) +
    Suppress('"')).setParseAction(asGrid) + Suppress('}')

pp_gridnode_vertex_name = Literal('normals') ^ Literal('offsets') ^ \
    Literal('offset_normals')
pp_gridnode_vertex_cont = Suppress('{') + ZeroOrMore(
    Suppress(QuotedString('"')) + Suppress('"') +
    Group(ZeroOrMore(pp_vertex_content)).setParseAction(asList) +
    Suppress('"')).setParseAction(asGrid) + Suppress('}')

pp_gridnode_float = Group(pp_gridnode_float_name + pp_gridnode_float_cont)
pp_gridnode_uint8 = Group(pp_gridnode_uint8_name + pp_gridnode_uint8_cont)
pp_gridnode_vertex = Group(pp_gridnode_vertex_name + pp_gridnode_vertex_cont)

pp_node_contents = Suppress('{') + \
    ZeroOrMore(pp_node_keyval ^ pp_gridnode_float ^
               pp_gridnode_uint8 ^ pp_gridnode_vertex ^
               pp_vnode).setParseAction(asList) + \
    Suppress('}')

pp_vnode <<= Group(pp_node_name + pp_node_contents)

pp_vmf = OneOrMore(pp_vnode)


def VmfParse(filename):
    results = []
    try:
        results = pp_vmf.parseFile(filename, encoding="iso-8859-1")
    except Exception as e:
        raise

    def make_node(node_result):
        name = node_result.pop(0)
        properties = [parse_property(p, name)
                      for p in node_result if isinstance(p, tuple)]
        subnodes = [make_node(n)
                    for n in node_result if isinstance(n, list)]
        node = VmfNode(name, properties, subnodes)
        return node

    return [make_node(r) for r in results]
