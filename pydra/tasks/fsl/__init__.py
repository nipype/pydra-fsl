"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

__all__ = [
    "BET",
    "ConcatXFM",
    "ConvertXFM",
    "FAST",
    "FLIRT",
    "FNIRT",
    "FSLMerge",
    "FSLReorient2Std",
    "FSLROI",
    "InvertXFM",
    "RobustFOV",
    "fslmaths",
]

from . import fslmaths
from .bet import BET
from .concat_xfm import ConcatXFM
from .convert_xfm import ConvertXFM
from .eddy import Eddy
from .fast import FAST
from .flirt import FLIRT
from .fnirt import FNIRT
from .fslmerge import FSLMerge
from .fslreorient2std import FSLReorient2Std
from .fslroi import FSLROI
from .invert_xfm import InvertXFM
from .robustfov import RobustFOV
