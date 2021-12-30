from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from future import standard_library
standard_library.install_aliases()

from decimal import Decimal


def _repr_prop_value(val, wrapper=None):
    vstr = val
    if isinstance(val, str):
        vstr = val
    elif isinstance(val, Decimal):
        vstr = '{:.6g}'.format(val)
    elif isinstance(val, bool):
        vstr = '1' if val else '0'
    elif isinstance(val, int):
        vstr = str(val)
    elif isinstance(val, list) or isinstance(val, tuple):
        vstr = ' '.join([_repr_prop_value(c) for c in val])

    if isinstance(wrapper, str) and len(wrapper):
        return wrapper[0] + vstr + wrapper[-1]
    return vstr


def _property_str(key, val, indent):
    return '   ' * indent + '"' + key + '" "' + val + '"' + '\n'


def write_property(prop, node_name=None, indent=0):

    key, pvalue = prop
    if (node_name == 'editor' and key == 'logicalpos') or \
       (node_name == 'dispinfo' and key == 'startposition'):
        pvalue = _repr_prop_value(pvalue, '[]')
    elif node_name == 'cordon' and key in ['mins', 'maxs']:
        pvalue = _repr_prop_value(pvalue, '()')
    elif node_name == 'side' and key in ['uaxis', 'vaxis']:
        pvalue = _repr_prop_value(pvalue[:4], '[]') + \
            ' ' + _repr_prop_value(pvalue[4])
    elif node_name == 'side' and key == 'plane':
        pvalue = ' '.join([_repr_prop_value(c, '()') for c in pvalue])
    elif node_name in ['normals', 'distances', 'offsets', 'offset_normals',
                       'alphas', 'triangle_tags'] and key == 'rows':
        rows = [('row' + str(index), _repr_prop_value(r))
                for index, r in enumerate(pvalue)]
        return ''.join([_property_str(r[0], r[1], indent) for r in rows])
    else:
        pvalue = _repr_prop_value(pvalue)

    return _property_str(key, pvalue, indent)
