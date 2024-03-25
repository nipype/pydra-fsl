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
from .flirt import (
    FLIRT,
    ApplyXFM,
    ConcatXFM,
    ConvertXFM,
    FixScaleSkew,
    Img2ImgCoord,
    Img2StdCoord,
    InvertXFM,
    Std2ImgCoord,
)
from .fnirt import FNIRT, ApplyWarp, ConvertWarp, FNIRTFileUtils, InvWarp
from .fugue import FUGUE, FSLPrepareFieldmap, Prelude, SigLoss
from .susan import SUSAN
from .utils import (
    FSLFFT,
    FSLROI,
    FSLChFileType,
    FSLInfo,
    FSLInterleave,
    FSLMerge,
    FSLOrient,
    FSLReorient2Std,
    FSLSelectVols,
    FSLSlice,
    FSLSmoothFill,
    FSLSplit,
    FSLSwapDim,
)
