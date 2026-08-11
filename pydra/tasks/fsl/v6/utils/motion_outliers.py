from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define
class MotionOutliers(shell.Task["MotionOutliers.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.motion_outliers import MotionOutliers

    >>> task = MotionOutliers()
    >>> task.in_file = Nifti1.mock("epi.nii")
    >>> task.mask = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "fsl_motion_outliers"
    in_file: Nifti1 = shell.arg(help="unfiltered 4D image", argstr="-i {in_file}")
    mask: File = shell.arg(help="mask image for calculating metric", argstr="-m {mask}")
    metric: ty.Any = shell.arg(
        help="metrics: refrms - RMS intensity difference to reference volume as metric [default metric], refmse - Mean Square Error version of refrms (used in original version of fsl_motion_outliers), dvars - DVARS, fd - frame displacement, fdrms - FD with RMS matrix calculation",
        argstr="--{metric}",
    )
    threshold: float = shell.arg(
        help="specify absolute threshold value (otherwise use box-plot cutoff = P75 + 1.5*IQR)",
        argstr="--thresh={threshold}",
    )
    no_motion_correction: bool = shell.arg(
        help="do not run motion correction (assumed already done)", argstr="--nomoco"
    )
    dummy: int = shell.arg(
        help="number of dummy scans to delete (before running anything and creating EVs)",
        argstr="--dummy={dummy}",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output outlier file name",
            argstr="-o {out_file}",
            path_template="{in_file}_outliers.txt",
        )
        out_metric_values: Path = shell.outarg(
            help="output metric values (DVARS etc.) file name",
            argstr="-s {out_metric_values}",
            path_template="{in_file}_metrics.txt",
        )
        out_metric_plot: Path = shell.outarg(
            help="output metric values plot (DVARS etc.) file name",
            argstr="-p {out_metric_plot}",
            path_template="{in_file}_metrics.png",
        )
