|python-versions| |travis-build| |appveyor-build| |docs|

pyaaf2
======

A python module for reading and writing Advanced Authoring Format (AAF) files.
pyaaf2 rewrite of `pyaaf1 <https://github.com/markreidvfx/pyaaf>`_ in pure python.

Features
--------

- Read/Write AAF files
- Modifying existing AAF files inplace
- Embedding DNxHD/DNxHR/WAV media
- Low level read/write Compound File Binary access
- Lazy file reading
- Zero dependencies, does not use AAF SDK

Requirements
------------

- Python >= 2.7

Installation
------------

You can install pyaaf2 via::

    pip install pyaaf2

or if you want to use the latest development git master::

    git clone https://github.com/markreidvfx/pyaaf2
    cd pyaaf2
    python setup.py install

Documentation
-------------

Documentation is available on `Read the Docs. <http://pyaaf.readthedocs.io/>`_

TODO
----

- More docs
- More tests
- More helper classes
- Port more pyaaf1 examples
- MXF linking improvements
- AMA linking improvements
- CFB red black tree
- XML support

.. |python-versions| image:: https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7-blue.svg

.. |travis-build| image:: https://travis-ci.org/markreidvfx/pyaaf2.svg?branch=master
    :alt: travis build status
    :target: https://travis-ci.org/markreidvfx/pyaaf2

.. |appveyor-build| image:: https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true
    :alt: appveyor build status
    :target: https://ci.appveyor.com/project/markreidvfx/pyaaf2

.. |docs| image:: https://readthedocs.org/projects/pyaaf/badge/?version=latest
    :alt: Documentation Status
    :target: http://pyaaf.readthedocs.io/en/latest/?badge=latest
