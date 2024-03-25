"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

from .bet import BET, RobustFOV
from .eddy import Eddy
from .fast import FAST
from .flirt import FLIRT, ApplyXFM, ConcatXFM, ConvertXFM, InvertXFM
from .fnirt import FNIRT, ApplyWarp, ConvertWarp, InvWarp
from .susan import SUSAN
from .utils import FSLROI, FSLMerge, FSLReorient2Std, fslmaths
