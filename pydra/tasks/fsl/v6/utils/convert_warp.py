from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


@shell.define(xor=[["abswarp", "relwarp"], ["out_abswarp", "out_relwarp"]])
class ConvertWarp(shell.Task["ConvertWarp.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.convert_warp import ConvertWarp

    >>> task = ConvertWarp()
    >>> task.reference = File.mock()
    >>> task.premat = File.mock()
    >>> task.warp1 = Nifti1.mock("warpfield.nii")
    >>> task.midmat = File.mock()
    >>> task.warp2 = File.mock()
    >>> task.postmat = File.mock()
    >>> task.shift_in_file = File.mock()
    >>> task.relwarp = True
    >>> task.cmdline
    'convertwarp --ref=T1.nii --rel --warp1=warpfield.nii --out=T1_concatwarp.nii.gz'


    """

    executable = "convertwarp"
    reference: File = shell.arg(
        help="Name of a file in target space of the full transform.",
        argstr="--ref={reference}",
        position=1,
    )
    premat: File = shell.arg(
        help="filename for pre-transform (affine matrix)", argstr="--premat={premat}"
    )
    warp1: Nifti1 = shell.arg(
        help="Name of file containing initial warp-fields/coefficients (follows premat). This could e.g. be a fnirt-transform from a subjects structural scan to an average of a group of subjects.",
        argstr="--warp1={warp1}",
    )
    midmat: File = shell.arg(
        help="Name of file containing mid-warp-affine transform",
        argstr="--midmat={midmat}",
    )
    warp2: File = shell.arg(
        help="Name of file containing secondary warp-fields/coefficients (after warp1/midmat but before postmat). This could e.g. be a fnirt-transform from the average of a group of subjects to some standard space (e.g. MNI152).",
        argstr="--warp2={warp2}",
    )
    postmat: File = shell.arg(
        help="Name of file containing an affine transform (applied last). It could e.g. be an affine transform that maps the MNI152-space into a better approximation to the Talairach-space (if indeed there is one).",
        argstr="--postmat={postmat}",
    )
    shift_in_file: File = shell.arg(
        help='Name of file containing a "shiftmap", a non-linear transform with displacements only in one direction (applied first, before premat). This would typically be a fieldmap that has been pre-processed using fugue that maps a subjects functional (EPI) data onto an undistorted space (i.e. a space that corresponds to his/her true anatomy).',
        argstr="--shiftmap={shift_in_file}",
    )
    shift_direction: ty.Any = shell.arg(
        help="Indicates the direction that the distortions from --shiftmap goes. It depends on the direction and polarity of the phase-encoding in the EPI sequence.",
        argstr="--shiftdir={shift_direction}",
        requires=["shift_in_file"],
    )
    cons_jacobian: bool = shell.arg(
        help="Constrain the Jacobian of the warpfield to lie within specified min/max limits.",
        argstr="--constrainj",
    )
    jacobian_min: float = shell.arg(
        help="Minimum acceptable Jacobian value for constraint (default 0.01)",
        argstr="--jmin={jacobian_min}",
    )
    jacobian_max: float = shell.arg(
        help="Maximum acceptable Jacobian value for constraint (default 100.0)",
        argstr="--jmax={jacobian_max}",
    )
    abswarp: bool = shell.arg(
        help="If set it indicates that the warps in --warp1 and --warp2 should be interpreted as absolute. I.e. the values in --warp1/2 are the coordinates in the next space, rather than displacements. This flag is ignored if --warp1/2 was created by fnirt, which always creates relative displacements.",
        argstr="--abs",
    )
    relwarp: bool = shell.arg(
        help="If set it indicates that the warps in --warp1/2 should be interpreted as relative. I.e. the values in --warp1/2 are displacements from the coordinates in the next space.",
        argstr="--rel",
    )
    out_abswarp: bool = shell.arg(
        help="If set it indicates that the warps in --out should be absolute, i.e. the values in --out are displacements from the coordinates in --ref.",
        argstr="--absout",
    )
    out_relwarp: bool = shell.arg(
        help="If set it indicates that the warps in --out should be relative, i.e. the values in --out are displacements from the coordinates in --ref.",
        argstr="--relout",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="Name of output file, containing warps that are the combination of all those given as arguments. The format of this will be a field-file (rather than spline coefficients) with any affine components included.",
            argstr="--out={out_file}",
            position=-1,
            path_template="{reference}_concatwarp",
        )
