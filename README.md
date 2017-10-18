pyaaf2
======

![Supported Versions](https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg)
[![Build Status](https://travis-ci.org/markreidvfx/pyaaf2.svg?branch=master)](https://travis-ci.org/markreidvfx/pyaaf2)

A rewrite of [pyaaf](https://github.com/markreidvfx/pyaaf) in pure python.
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

- Better memory management
- Cleanup object attach/detach code
- Sphinx docs
- More helper classes
- MXF linking helpers
- Port pyaaf1 examples
- More tests
- CFB/Stream shrinking
