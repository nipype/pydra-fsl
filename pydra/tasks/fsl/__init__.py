"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

__all__ = [
    "BET",
    "Eddy",
    "FAST",
    "FNIRT",
    "FSLMerge",
    "FSLReorient2Std",
    "FSLROI",
    "RobustFOV",
    "flirt",
    "fslmaths",
]

from . import flirt, fslmaths
from .bet import BET
from .eddy import Eddy
from .fast import FAST
from .fnirt import FNIRT
from .fslmerge import FSLMerge
from .fslreorient2std import FSLReorient2Std
from .fslroi import FSLROI
from .robustfov import RobustFOV

__all__ += flirt.__all__
