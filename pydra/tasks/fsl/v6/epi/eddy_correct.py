from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def eddy_corrected_callable(output_dir, inputs, stdout, stderr):
    return inputs.out_file


@shell.define
class EddyCorrect(shell.Task["EddyCorrect.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.epi.eddy_correct import EddyCorrect

    >>> task = EddyCorrect()
    >>> task.in_file = Nifti1.mock("diffusion.nii")
    >>> task.out_file = "diffusion_edc.nii"
    >>> task.ref_num = 0
    >>> task.cmdline
    'eddy_correct diffusion.nii diffusion_edc.nii 0'


    """

    executable = "eddy_correct"
    in_file: Nifti1 = shell.arg(help="4D input file", argstr="{in_file}", position=1)
    out_file: Path = shell.arg(help="4D output file", argstr="{out_file}", position=2)
    ref_num: int | None = shell.arg(
        help="reference number", argstr="{ref_num}", position=3, default=0
    )

    class Outputs(shell.Outputs):
        eddy_corrected: File | None = shell.out(
            help="path/name of 4D eddy corrected output file",
            callable=eddy_corrected_callable,
        )
