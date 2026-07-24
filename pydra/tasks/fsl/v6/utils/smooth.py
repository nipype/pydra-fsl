from fileformats.generic import File
import logging
import numpy as np
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "fwhm":
        sigma = float(value) / np.sqrt(8 * np.log(2))
        pass

    return argstr.format(**inputs)


def fwhm_formatter(field, inputs):
    return _format_arg("fwhm", field, inputs, argstr="-kernel gauss {fwhm:.03} -fmean")


@shell.define(xor=[["fwhm", "sigma"]])
class Smooth(shell.Task["Smooth.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.smooth import Smooth

    >>> task = Smooth()
    >>> task.in_file = File.mock()
    >>> task.sigma = 8.0
    >>> task.cmdline
    'fslmaths functional2.nii -kernel gauss 8.000 -fmean functional2_smooth.nii.gz'


    >>> task = Smooth()
    >>> task.in_file = File.mock()
    >>> task.fwhm = 8.0
    >>> task.cmdline
    'fslmaths functional2.nii -kernel gauss 3.397 -fmean functional2_smooth.nii.gz'


    >>> task = Smooth()
    >>> task.in_file = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "fslmaths"
    in_file: File = shell.arg(help="", argstr="{in_file}", position=1)
    sigma: float | None = shell.arg(
        help="gaussian kernel sigma in mm (not voxels)",
        argstr="-kernel gauss {sigma:.03} -fmean",
        position=2,
    )
    fwhm: float | None = shell.arg(
        help="gaussian kernel fwhm, will be converted to sigma in mm (not voxels)",
        formatter=fwhm_formatter,
        position=2,
    )

    class Outputs(shell.Outputs):
        smoothed_file: Path = shell.outarg(
            help="",
            argstr="{smoothed_file}",
            path_template="{in_file}_smooth",
            position=3,
        )
