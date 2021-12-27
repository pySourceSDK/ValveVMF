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

import os  # NOQA: E402
from decimal import Decimal
from pyparsing import *  # NOQA: E402
from valvevmf.vmf import *  # NOQA: E402
from valvevmf.node import VMFNode  # NOQA: E402


def asTuple(data):
    return [tuple(data.asList()[0])]


def asList(data):
    return list(data.asList())


def asGrid(data):
    return ('rows', [d for d in data])


# Property parsing
pp_bool = Word(nums+'-').setParseAction(lambda p: bool(int(p[0])))
pp_int = Word(nums+'-').setParseAction(lambda p: int(p[0]))
pp_uint8 = Word(nums).setParseAction(lambda p: min(255, max(0, int(p[0]))))
pp_float = Word(nums+'-.').setParseAction(lambda p: Decimal(p[0]))


pp_angle = Group(pp_float + pp_float + pp_float).setParseAction(asTuple)
pp_origin = pp_angle

pp_vertex_content = Group(pp_float + pp_float +
                          pp_float).setParseAction(asTuple)
pp_vertex_tup = Suppress('(') + pp_vertex_content + Suppress(')')
pp_vertex_arr = Suppress('[') + pp_vertex_content + Suppress(']')

pp_plane = Group(pp_vertex_tup + pp_vertex_tup +
                 pp_vertex_tup).setParseAction(asTuple)
pp_color255 = Group(pp_uint8 + pp_uint8 + pp_uint8).setParseAction(asTuple)

pp_uvaxis = Group(Suppress('[') + pp_float + pp_float + pp_float + pp_float +
                  Suppress(']') + pp_float).setParseAction(asTuple)
pp_2dvector = Suppress('[') + Group(pp_float + pp_float) + Suppress(']')

pp_allowed_verts = Group(ZeroOrMore(pp_int)).setParseAction(asTuple)


# Node parsing
pp_vnode = Forward()
pp_node_name = Word(alphas+'_')
pp_node_keyval = Group(QuotedString('"') + QuotedString('"'))
pp_node_keyval.setParseAction(asTuple)

pp_gridnode_float_name = Literal('distances')
pp_gridnode_float_cont = Suppress('{') + ZeroOrMore(
    Suppress(QuotedString('"')) + Suppress('"') +
    Group(ZeroOrMore(pp_float)).setParseAction(asList) +
    Suppress('"')).setParseAction(asGrid) + Suppress('}')


pp_gridnode_uint8_name = Literal('alphas') ^ Literal('triangle_tags')
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

pp_vmf = ZeroOrMore(pp_vnode)


param_type_map = {
    'id': pp_int,
    'look': pp_vertex_arr,

    'entity': {
        'classname': None,
        'targetname': None,
        'comment': None,
        'angles': pp_angle,
        'origin': pp_origin,

        'position': pp_vertex_arr,
    },
    'versioninfo': {
        'prefab': pp_bool,
        'editorversion': pp_int,
        'editorbuild': pp_int,
        'mapversion': pp_int,
        'formatversion': pp_int,
    },
    'viewsettings': {
        'bSnapToGrid': pp_bool,
        'bShowGrid': pp_bool,
        'bShowLogicalGrid': pp_bool,
        'bShow3DGrid': pp_bool,
        'nGridSpacing': pp_int,
    },
    "world": {
        'maxpropscreenwidth': pp_int,
        'detailmaterial': None,
        'detailvbsp': None,
        'skyname': None,
    },
    'visgroup': {
        'name': None,
        'color': pp_color255,
        'visgroupid': pp_int,
    },
    'editor': {
        'color': pp_color255,
        'groupid': pp_int,
        'visgroupid': pp_int,
        'visgroupshown': pp_bool,
        'visgroupautoshown': pp_bool,
        'logicalpos': pp_2dvector,

    },
    'side': {
        'plane': pp_plane,
        'material': None,
        'uaxis': pp_uvaxis,
        'vaxis': pp_uvaxis,
        'rotation': pp_float,
        'lightmapscale': pp_int,
        'smoothing_groups': pp_int,
    },
    'dispinfo': {
        'power': pp_int,
        'startposition': pp_vertex_arr,
        'flags': pp_int,
        'elevation': pp_int,
        'subdiv': pp_bool,
    },
    'allowed_verts': {
        '10': pp_allowed_verts,
    },
    'cameras': {
        'activecamera': pp_int,
    },
    'cordon': {
        'active': pp_bool,
        'mins': pp_vertex_tup,
        'maxs': pp_vertex_tup,
    }
}


def VmfParse(filename):
    results = []
    try:
        results = pp_vmf.parseFile(filename, encoding="iso-8859-1")
    except Exception as e:
        raise

    def read_prop(node_name, keyvalue):
        key, value = keyvalue
        target_dict = param_type_map
        prop_parser = target_dict.get(key, None)
        target_dict = target_dict.get(node_name, target_dict)
        prop_parser = target_dict.get(key, prop_parser)

        if prop_parser:
            value = prop_parser.parse_string(value)[0]
        return (key, value)

    def make_node(node_result):
        name = node_result.pop(0)
        properties = [read_prop(name, p)
                      for p in node_result if isinstance(p, tuple)]
        subnodes = [make_node(n)
                    for n in node_result if isinstance(n, list)]
        node = VMFNode(name, properties, subnodes)
        return node

    return [make_node(r) for r in results]
