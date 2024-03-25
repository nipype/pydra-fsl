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

from . import maths
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
from .fugue import FUGUE, Prelude, PrepareFieldmap, SigLoss
from .susan import SUSAN
from .utils import (
    FFT,
    ROI,
    ChFileType,
    Info,
    Interleave,
    Merge,
    Orient,
    Reorient2Std,
    SelectVols,
    Slice,
    SmoothFill,
    Split,
    SwapDim,
)

# TODO: Drop compatibility aliases when 0.x is released.
FSLFFT = FFT
FSLROI = ROI
FSLChFileType = ChFileType
FSLInfo = Info
FSLInterleave = Interleave
FSLMerge = Merge
FSLOrient = Orient
FSLPrepareFieldmap = PrepareFieldmap
FSLReorient2Std = Reorient2Std
FSLSelectVols = SelectVols
FSLSlice = Slice
FSLSmoothFill = SmoothFill
FSLSplit = Split
FSLSwapDim = SwapDim
fslmaths = maths
