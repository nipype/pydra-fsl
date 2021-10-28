"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.TODO
"""
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
