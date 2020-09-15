# Copyright (C) 2020  SymbiFlow Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

# The top directory where environment will be created.
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

# A pip `requirements.txt` file.
# https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
REQUIREMENTS_FILE := requirements.txt

# A conda `environment.yml` file.
# https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
ENVIRONMENT_FILE := environment.yml

include third_party/make-env/conda.mk

# Build the package locally

build: $(CONDA_ENV_PYTHON)
	$(IN_CONDA_ENV) python setup.py sdist bdist_wheel && twine check dist/*

build-clean:
	rm -rf env/downloads/conda-pkgs
	rm -rf build dist *.egg-info
	find -name *.pyc -delete
	find -name __pycache__ -delete

.PHONY: build build-clean

clean:: build-clean
