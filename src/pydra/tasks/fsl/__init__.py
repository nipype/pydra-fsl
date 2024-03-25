"""
This is a basic doctest demonstrating that the package and pydra can both be successfully
imported.

FSL interfaces are available within the `pydra.tasks.fsl` package.

>>> from pydra.tasks import fsl

.. automodule:: pydra.tasks.fsl.bet
.. automodule:: pydra.tasks.fsl.eddy
.. automodule:: pydra.tasks.fsl.fast
.. automodule:: pydra.tasks.fsl.flirt
.. automodule:: pydra.tasks.fsl.fnirt
.. automodule:: pydra.tasks.fsl.fslmaths
.. automodule:: pydra.tasks.fsl.fugue
.. automodule:: pydra.tasks.fsl.susan
.. automodule:: pydra.tasks.fsl.utils
"""

from . import fslmaths
from .bet import BET, RobustFOV
from .eddy import ApplyTopup, Eddy, Topup
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
