"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

__all__ = [
    "BET",
    "ConvertXFM",
    "FAST",
    "FLIRT",
    "FNIRT",
    "FSLMerge",
    "FSLReorient2Std",
    "FSLROI",
    "RobustFOV",
]

from .bet import BET
from .convert_xfm import ConvertXFM
from .eddy import Eddy
from .fast import FAST
from .flirt import FLIRT
from .fnirt import FNIRT
from .fslmerge import FSLMerge
from .fslreorient2std import FSLReorient2Std
from .fslroi import FSLROI
from .robustfov import RobustFOV
