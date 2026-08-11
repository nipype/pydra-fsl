import attrs
from fileformats.generic import File
from fileformats.medimage import NiftiGz
import logging
from pydra.compose import shell


logger = logging.getLogger(__name__)


def aggregate_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    needed_outputs = ["dlh", "volume", "resels"]

    outputs = {}
    stdout = stdout.split("\n")
    outputs["dlh"] = float(stdout[0].split()[1])
    outputs["volume"] = int(stdout[1].split()[1])
    outputs["resels"] = float(stdout[2].split()[1])
    return outputs


def dlh_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dlh")


def volume_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("volume")


def resels_callable(output_dir, inputs, stdout, stderr):
    outputs = aggregate_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("resels")


@shell.define(xor=[["dof", "zstat_file"]])
class SmoothEstimate(shell.Task["SmoothEstimate.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import NiftiGz
    >>> from pydra.tasks.fsl.v6.model.smooth_estimate import SmoothEstimate

    >>> task = SmoothEstimate()
    >>> task.mask_file = File.mock()
    >>> task.residual_fit_file = File.mock()
    >>> task.zstat_file = NiftiGz.mock("zstat1.nii.gz")
    >>> task.cmdline
    'smoothest --mask=mask.nii --zstat=zstat1.nii.gz'


    """

    executable = "smoothest"
    dof: int | None = shell.arg(
        help="number of degrees of freedom", argstr="--dof={dof}"
    )
    mask_file: File = shell.arg(help="brain mask volume", argstr="--mask={mask_file}")
    residual_fit_file: File | None = shell.arg(
        help="residual-fit image file",
        argstr="--res={residual_fit_file}",
        requires=["dof"],
    )
    zstat_file: NiftiGz | None = shell.arg(
        help="zstat image file", argstr="--zstat={zstat_file}"
    )

    class Outputs(shell.Outputs):
        dlh: float | None = shell.out(
            help="smoothness estimate sqrt(det(Lambda))", callable=dlh_callable
        )
        volume: int | None = shell.out(
            help="number of voxels in mask", callable=volume_callable
        )
        resels: float | None = shell.out(
            help="volume of resel, in voxels, defined as FWHM_x * FWHM_y * FWHM_z",
            callable=resels_callable,
        )
