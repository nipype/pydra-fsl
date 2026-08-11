from fileformats.generic import File
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define
class RobustFOV(shell.Task["RobustFOV.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.robust_fov import RobustFOV

    """

    executable = "robustfov"
    in_file: File = shell.arg(help="input filename", argstr="-i {in_file}", position=1)
    brainsize: int = shell.arg(
        help="size of brain in z-dimension (default 170mm/150mm)",
        argstr="-b {brainsize}",
    )

    class Outputs(shell.Outputs):
        out_roi: Path = shell.outarg(
            help="ROI volume output name",
            argstr="-r {out_roi}",
            path_template="{in_file}_ROI",
        )
        out_transform: Path = shell.outarg(
            help="Transformation matrix in_file to out_roi output name",
            argstr="-m {out_transform}",
            path_template="{in_file}_to_ROI",
        )
