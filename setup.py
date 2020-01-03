#!/usr/bin/env python
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
version = os.path.join(here, 'protonvpn_gtk', '__version__.py')

about = {}
with open(version, 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["protonvpn-gtk = protonvpn_gtk.run:main"]
        },
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    url=about['__url__'],
    install_requires=[
        'protonvpn-cli>=2.2.0',
        'PyGObject>=3.34.0'
    ],
    data_files=[
        ('icons', ['icons/proto.png']),
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: GTK',
        'Topic :: Security',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
