"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

__all__ = [
    "Eddy",
    "FAST",
    "FNIRT",
    "FSLMerge",
    "FSLReorient2Std",
    "FSLROI",
    "fslmaths",
]

from . import bet, flirt, fslmaths
from .eddy import Eddy
from .fast import FAST
from .fnirt import FNIRT
from .fslmerge import FSLMerge
from .fslreorient2std import FSLReorient2Std
from .fslroi import FSLROI

__all__ += bet.__all__
__all__ += flirt.__all__
