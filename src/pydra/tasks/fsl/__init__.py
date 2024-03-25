"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

>>> import pydra.engine
>>> import pydra.tasks.fsl
"""

from .bet import BET, RobustFOV
from .eddy import Eddy
from .fast import FAST
from .flirt import (
    FLIRT,
    ApplyXFM,
    ConcatXFM,
    ConvertXFM,
    Img2ImgCoord,
    Img2StdCoord,
    InvertXFM,
    Std2ImgCoord,
)
from .fnirt import FNIRT, ApplyWarp, ConvertWarp, FNIRTFileUtils, InvWarp
from .fugue import FUGUE
from .susan import SUSAN
from .utils import (
    FSLFFT,
    FSLROI,
    FSLChFileType,
    FSLInfo,
    FSLInterleave,
    FSLMerge,
    FSLReorient2Std,
    FSLSlice,
    FSLSplit,
    FSLSwapDim,
    fslmaths,
)