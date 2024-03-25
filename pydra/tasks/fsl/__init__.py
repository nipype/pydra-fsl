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
        "pydra-fsl has not been properly installed, please run "
        f"`pip install -e {str(pkg_path)}` to install a development version"
    )
if "nipype" not in __version__:
    try:
        from .auto._version import nipype_version, nipype2pydra_version
    except ImportError:
        warn(
            "Nipype interfaces haven't been automatically converted from their specs in "
            f"`nipype-auto-conv`. Please run `{str(pkg_path / 'nipype-auto-conv' / 'generate')}` "
            "to generated the converted Nipype interfaces in pydra.tasks.fsl.auto"
        )
    else:
        n_ver = nipype_version.replace(".", "_")
        n2p_ver = nipype2pydra_version.replace(".", "_")
        __version__ += (
            "_" if "+" in __version__ else "+"
        ) + f"nipype{n_ver}_nipype2pydra{n2p_ver}"


__all__ = ["__version__"]
