|python-versions| |travis-build| |appveyor-build| |docs|

PyAAF 2.0
=========

A rewrite of `pyaaf <https://github.com/markreidvfx/pyaaf>`_ in pure python.
Still a work in progress, but getting pretty close to being feature complete
with pyaaf.

Features
--------

- Read/Write AAF files
- Modifying existing AAF files inplace
- Embedding DNxHD/DNxHR/WAV media
- Low level read/write Compound File Binary access
- Lazy file reading
- Zero dependencies

Requirements
------------

- Python >= 2.7

TODO
----

- More docs
- More tests
- More helper classes
- Port pyaaf1 examples
- MXF linking improvements
- AMA linking improvements
- CFB stream shrinking
- CFB red black tree

Have fun, `Read the Docs <http://pyaaf.readthedocs.io/>`_ and good luck!

.. |python-versions| image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg

.. |travis-build| image:: https://travis-ci.org/markreidvfx/pyaaf2.svg?branch=master
    :alt: travis build status
    :target: https://travis-ci.org/markreidvfx/pyaaf2

.. |appveyor-build| image:: https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true
    :alt: appveyor build status
    :target: https://ci.appveyor.com/project/markreidvfx/pyaaf2

.. |docs| image:: https://readthedocs.org/projects/pyaaf/badge/?version=latest
    :alt: Documentation Status
    :target: http://pyaaf.readthedocs.io/en/latest/?badge=latest
