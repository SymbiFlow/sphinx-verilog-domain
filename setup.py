#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020  The SymbiFlow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import sys
from os import path

import setuptools

__dir__ = path.dirname(path.abspath(__file__))

# Manually import the version number so dependencies don't need to be installed
# when running setup.py
version_file = path.join(__dir__, "sphinx_verilog_domain", "version.py")
if path.exists(version_file):
    exec(open(version_file).read())
else:
    __version__ = "0.0.dev0"

with open("README.rst", "r") as fh:
    long_description = fh.read()

install_requires = [
    'setuptools',
    'docutils',
    'sphinx',
    'lark-parser'
]

setuptools.setup(
    name="sphinx-verilog-domain",
    version=__version__,
    author="SymbiFlow Authors",
    author_email="symbiflow@lists.librecores.org",
    #license="Apache 2.0",
    description="Verilog Domain for Sphinx",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/SymbiFlow/sphinx-verilog-domain",
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    package_data={'': ["verilog.lark"]},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        'Natural Language :: English',
        'Topic :: Documentation :: Sphinx',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
    ],
    install_requires=install_requires,
)
