#!/usr/bin/env python
import sys

from setuptools import setup, find_packages
import versioneer

SUBPACKAGE = "fsl"

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ["setuptools >= 30.3.0"]
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []

if __name__ == "__main__":
    setup(
        name=f"pydra-{SUBPACKAGE}",
        setup_requires=SETUP_REQUIRES,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        packages=[
            f"pydra.tasks.{SUBPACKAGE}.{package}"
            for package in find_packages("pydra/tasks/{SUBPACKAGE}")
        ],
    )
