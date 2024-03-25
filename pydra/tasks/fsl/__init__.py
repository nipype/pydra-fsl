"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

from . import fslmaths
from .bet import BET, RobustFOV
from .eddy import Eddy
from .fast import FAST
from .flirt import FLIRT, ApplyXFM, ConcatXFM, ConvertXFM, InvertXFM
from .fnirt import FNIRT
from .fslmerge import FSLMerge
from .fslreorient2std import FSLReorient2Std
from .fslroi import FSLROI
from .susan import SUSAN
