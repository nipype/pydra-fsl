"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

from warnings import warn
from pathlib import Path

pkg_path = Path(__file__).parent.parent

try:
    from ._version import __version__
except ImportError:
    raise RuntimeError(
        "pydra-tasks-fsl has not been properly installed, please run "
        f"`pip install -e {str(pkg_path)}` to install a development version"
    )

__all__ = ["__version__"]
