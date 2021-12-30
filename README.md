[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/pySourceSDK/ValveVMF/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/valvevmf.svg)](https://pypi.python.org/pypi/valvevmf/)
[![PyPI version fury.io](https://badge.fury.io/py/valvevmf.svg)](https://pypi.python.org/pypi/valvevmf/)
[![alt text](https://github.com/pySourceSDK/ValveVMF/blob/master/docs/source/coverage.svg "coverage")]()

# ValveVMF

ValveVMF is a Python library for parsing .vmf files for the Source Engine. It provides ways to read, modify and write vmf files.

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

Here's a few example usage of valveVmf

### Parsing

Parsing can be done by creating an instance of Vmf with a path.

```python
>>> from valvevmf import Vmf

>>> vmf = Vmf('C:/mapsrc/yourmap.vmf')
>>> print(vmf.nodes)
>>> vmf.save()
```
