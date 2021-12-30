Quickstart
==========

Get yourself up and running quickly.

Installation
------------

PyPI
~~~~
ValveVMF is available on the Python Package Index. This makes installing it with pip as easy as:

.. code-block:: bash

   pip3 install valvevmf

Git
~~~

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

.. code-block:: bash

   git clone git://github.com/pySourceSDK/ValveVMF.git

and install it from the repo directory with:

.. code-block:: bash

   python3 setup.py install

Usage
-----

Here's a few example usage of ValveVMF

Parsing
~~~~~~~

Parsing can be done by creating an instance of Vmf with a path.

.. code-block:: python

   > from valvevmf import Vmf

   > vmf = Vmf('C:/mapsrc/yourmap.vmf')
   > print(vmf.nodes)
   > vmf.save()
