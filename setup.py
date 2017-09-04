import sys

from setuptools import setup

setup(
    name='PyAAF2',
    version='2.0.0',
    description='Read and Write Advanced Authoring Format Files',
    author='Mark Reid',
    author_email='mindmark@gmail.com',
    url='https://github.com/markreidvfx/pyaaf2',

    packages=[
        'aaf2',
        'aaf2.model',
    ],
)
