from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


@shell.define(xor=[["absolute", "relative"]])
class InvWarp(shell.Task["InvWarp.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.inv_warp import InvWarp

    >>> task = InvWarp()
    >>> task.warp = Nifti1.mock("struct2mni.nii")
    >>> task.reference = File.mock()
    >>> task.cmdline
    'invwarp --out=struct2mni_inverse.nii.gz --ref=anatomical.nii --warp=struct2mni.nii'


    """

    executable = "invwarp"
    warp: Nifti1 = shell.arg(
        help="Name of file containing warp-coefficients/fields. This would typically be the output from the --cout switch of fnirt (but can also use fields, like the output from --fout).",
        argstr="--warp={warp}",
    )
    reference: File = shell.arg(
        help="Name of a file in target space. Note that the target space is now different from the target space that was used to create the --warp file. It would typically be the file that was specified with the --in argument when running fnirt.",
        argstr="--ref={reference}",
    )
    absolute: bool = shell.arg(
        help="If set it indicates that the warps in --warp should be interpreted as absolute, provided that it is not created by fnirt (which always uses relative warps). If set it also indicates that the output --out should be absolute.",
        argstr="--abs",
    )
    relative: bool = shell.arg(
        help="If set it indicates that the warps in --warp should be interpreted as relative. I.e. the values in --warp are displacements from the coordinates in the --ref space. If set it also indicates that the output --out should be relative.",
        argstr="--rel",
    )
    niter: int = shell.arg(
        help="Determines how many iterations of the gradient-descent search that should be run.",
        argstr="--niter={niter}",
    )
    regularise: float = shell.arg(
        help="Regularization strength (default=1.0).",
        argstr="--regularise={regularise}",
    )
    noconstraint: bool = shell.arg(
        help="Do not apply Jacobian constraint", argstr="--noconstraint"
    )
    jacobian_min: float = shell.arg(
        help="Minimum acceptable Jacobian value for constraint (default 0.01)",
        argstr="--jmin={jacobian_min}",
    )
    jacobian_max: float = shell.arg(
        help="Maximum acceptable Jacobian value for constraint (default 100.0)",
        argstr="--jmax={jacobian_max}",
    )

    class Outputs(shell.Outputs):
        inverse_warp: Path = shell.outarg(
            help='Name of output file, containing warps that are the "reverse" of those in --warp. This will be a field-file (rather than a file of spline coefficients), and it will have any affine component included as part of the displacements.',
            argstr="--out={inverse_warp}",
            path_template="{warp}_inverse",
        )
