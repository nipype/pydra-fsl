import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []
    self_dict = {}

    if skip is None:
        skip = []

    suffix = "field"
    if (inputs["out_format"] is not attrs.NOTHING) and inputs["out_format"] == "spline":
        suffix = "coeffs"

    trait_spec = self_dict["inputs"].trait("out_file")
    trait_spec.name_template = "%s_" + suffix

    if inputs["write_jacobian"]:
        if inputs["out_jacobian"] is attrs.NOTHING:
            jac_spec = self_dict["inputs"].trait("out_jacobian")
            jac_spec.name_source = ["in_file"]
            jac_spec.name_template = "%s_jac"
            jac_spec.output_name = "out_jacobian"
    else:
        skip += ["out_jacobian"]

    skip += ["write_jacobian"]

    return parsed_inputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    return inputs.out_file


def out_jacobian_callable(output_dir, inputs, stdout, stderr):
    parsed_inputs = _parse_inputs(inputs)
    return parsed_inputs.get("out_jacobian", attrs.NOTHING)


@shell.define
class WarpUtils(shell.Task["WarpUtils.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.warp_utils import WarpUtils

    >>> task = WarpUtils()
    >>> task.in_file = Nifti1.mock("warpfield.nii")
    >>> task.reference = File.mock()
    >>> task.out_format = "spline"
    >>> task.cmdline
    'fnirtfileutils --in=warpfield.nii --outformat=spline --ref=T1.nii --warpres=10.0000,10.0000,10.0000 --out=warpfield_coeffs.nii.gz'


    """

    executable = "fnirtfileutils"
    in_file: Nifti1 = shell.arg(
        help="Name of file containing warp-coefficients/fields. This would typically be the output from the --cout switch of fnirt (but can also use fields, like the output from --fout).",
        argstr="--in={in_file}",
    )
    reference: File = shell.arg(
        help="Name of a file in target space. Note that the target space is now different from the target space that was used to create the --warp file. It would typically be the file that was specified with the --in argument when running fnirt.",
        argstr="--ref={reference}",
    )
    out_format: ty.Any = shell.arg(
        help="Specifies the output format. If set to field (default) the output will be a (4D) field-file. If set to spline the format will be a (4D) file of spline coefficients.",
        argstr="--outformat={out_format}",
    )
    warp_resolution: ty.Any = shell.arg(
        help="Specifies the resolution/knot-spacing of the splines pertaining to the coefficients in the --out file. This parameter is only relevant if --outformat is set to spline. It should be noted that if the --in file has a higher resolution, the resulting coefficients will pertain to the closest (in a least-squares sense) file in the space of fields with the --warpres resolution. It should also be noted that the resolution will always be an integer multiple of the voxel size.",
        argstr="--warpres={warp_resolution[0]:0.4},{warp_resolution[1]:0.4},{warp_resolution[2]:0.4}",
    )
    knot_space: ty.Any = shell.arg(
        help="Alternative (to --warpres) specification of the resolution of the output spline-field.",
        argstr="--knotspace={knot_space[0]},{knot_space[1]},{knot_space[2]}",
    )
    out_file: Path = shell.arg(
        help="Name of output file. The format of the output depends on what other parameters are set. The default format is a (4D) field-file. If the --outformat is set to spline the format will be a (4D) file of spline coefficients.",
        argstr="--out={out_file}",
        position=-1,
    )
    write_jacobian: bool | None = shell.arg(
        help="Switch on --jac flag with automatically generated filename", default=False
    )
    out_jacobian: Path = shell.arg(
        help="Specifies that a (3D) file of Jacobian determinants corresponding to --in should be produced and written to filename.",
        argstr="--jac={out_jacobian}",
    )
    with_affine: bool = shell.arg(
        help="Specifies that the affine transform (i.e. that which was specified for the --aff parameter in fnirt) should be included as displacements in the --out file. That can be useful for interfacing with software that cannot decode FSL/fnirt coefficient-files (where the affine transform is stored separately from the displacements).",
        argstr="--withaff",
    )

    class Outputs(shell.Outputs):
        out_file: File | None = shell.out(
            help="Name of output file, containing the warp as field or coefficients.",
            callable=out_file_callable,
        )
        out_jacobian: File | None = shell.out(
            help="Name of output file, containing the map of the determinant of the Jacobian",
            callable=out_jacobian_callable,
        )
