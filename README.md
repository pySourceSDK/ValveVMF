[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/pySourceSDK/ValveVMF/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/valvevmf.svg)](https://pypi.python.org/pypi/valvevmf/)
[![Platforms](https://img.shields.io/badge/platform-Linux,_MacOS,_Windows-blue)]()
[![PyPI version fury.io](https://badge.fury.io/py/valvevmf.svg)](https://pypi.python.org/pypi/valvevmf/)
[![GitHub Workflow Status (with event)](https://github.com/pySourceSDK/ValveVMF/actions/workflows/tests.yml/badge.svg)]()
[![Test coverage](https://github.com/pySourceSDK/ValveVMF/blob/master/docs/source/coverage.svg "coverage")]()

# ValveVMF

ValveVMF is a python library for parsing and editing .VMF asset files associated with Valve's Source engine. It provides provides access to lump data in map files.

Full documentation: https://pysourcesdk.github.io/ValveVMF/

## Installation

### PyPI

ValveVMF is available on the Python Package Index. This makes installing it with pip as easy as:

```bash
pip3 install valvevmf
```

### Git

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

```bash
git clone git@github.com:pySourceSDK/ValveVMF.git
```

and install it with:

```bash
python3 setup.py install
```

## Usage

Here's a few example usage of ValveVMF

### Parsing

Parsing can be done by creating an instance of Vmf with a path.

```python
>>> from valvevmf import Vmf

>>> vmf = Vmf('C:/mapsrc/yourmap.vmf')
>>> print(vmf.nodes)
>>> vmf.save()
```
