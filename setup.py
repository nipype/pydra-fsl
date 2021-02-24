#!/usr/bin/env python
import sys

from setuptools import setup
import versioneer

SUBPACKAGE = "TODO"

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# 40.1.0 enables the `find_namespace:` directive
# Should match pyproject.toml
SETUP_REQUIRES = ["setuptools >= 40.1.0"]
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []

if __name__ == "__main__":
    setup(
        name=f"pydra-{SUBPACKAGE}",
        setup_requires=SETUP_REQUIRES,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
    )
