from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int
from future import standard_library
standard_library.install_aliases()

from pyparsing import *  # NOQA: E402
from decimal import Decimal  # NOQA: E402


def asTuple(data):
    return [tuple(data.asList()[0])]


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
pp_2dvector = Group(Suppress('[') + pp_float + pp_float +
                    Suppress(']')).setParseAction(asTuple)

pp_allowed_verts = Group(ZeroOrMore(pp_int)).setParseAction(asTuple)

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


def parse_property(keyvalue, node_name=None):
    key, value = keyvalue
    target_dict = param_type_map
    prop_parser = target_dict.get(key, None)
    if node_name:
        target_dict = target_dict.get(node_name, target_dict)
    prop_parser = target_dict.get(key, prop_parser)

    if prop_parser:
        value = prop_parser.parse_string(value)[0]
    return (key, value)
