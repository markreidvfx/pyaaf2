import sys

from setuptools import setup

setup(
    name='pyaaf2',
    version='1.0.0-dev4',
    description='Read and Write Advanced Authoring Format Files',
    author='Mark Reid',
    author_email='mindmark@gmail.com',
    url='https://github.com/markreidvfx/pyaaf2',
    project_urls={
        'Source':
            'https://github.com/markreidvfx/pyaaf2',
        'Documentation':
            'http://pyaaf.readthedocs.io',
        'Issues':
            'https://github.com/markreidvfx/pyaaf2/issues',
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='film tv editing editorial edit non-linear edl time',

    platforms='any',

    packages=[
        'aaf2',
        'aaf2.model',
        'aaf2.model.ext',
    ],
)
