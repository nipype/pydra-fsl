import attrs
from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )[name]
    else:
        return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class VecReg(shell.Task["VecReg.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.datascience import TextMatrix
    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.dti.vec_reg import VecReg

    >>> task = VecReg()
    >>> task.in_file = Nifti1.mock("diffusion.nii")
    >>> task.out_file = "diffusion_vreg.nii"
    >>> task.ref_vol = Nifti1.mock("mni.nii")
    >>> task.affine_mat = TextMatrix.mock("trans.mat")
    >>> task.warp_field = File.mock()
    >>> task.rotation_mat = File.mock()
    >>> task.rotation_warp = File.mock()
    >>> task.mask = File.mock()
    >>> task.ref_mask = File.mock()
    >>> task.cmdline
    'vecreg -t trans.mat -i diffusion.nii -o diffusion_vreg.nii -r mni.nii'


    """

    executable = "vecreg"
    in_file: Nifti1 = shell.arg(
        help="filename for input vector or tensor field", argstr="-i {in_file}"
    )
    ref_vol: Nifti1 = shell.arg(
        help="filename for reference (target) volume", argstr="-r {ref_vol}"
    )
    affine_mat: TextMatrix = shell.arg(
        help="filename for affine transformation matrix", argstr="-t {affine_mat}"
    )
    warp_field: File = shell.arg(
        help="filename for 4D warp field for nonlinear registration",
        argstr="-w {warp_field}",
    )
    rotation_mat: File = shell.arg(
        help="filename for secondary affine matrix if set, this will be used for the rotation of the vector/tensor field",
        argstr="--rotmat={rotation_mat}",
    )
    rotation_warp: File = shell.arg(
        help="filename for secondary warp field if set, this will be used for the rotation of the vector/tensor field",
        argstr="--rotwarp={rotation_warp}",
    )
    interpolation: ty.Any = shell.arg(
        help="interpolation method : nearestneighbour, trilinear (default), sinc or spline",
        argstr="--interp={interpolation}",
    )
    mask: File = shell.arg(help="brain mask in input space", argstr="-m {mask}")
    ref_mask: File = shell.arg(
        help="brain mask in output space (useful for speed up of nonlinear reg)",
        argstr="--refmask={ref_mask}",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="filename for output registered vector or tensor field",
            argstr="-o {out_file}",
            path_template='"diffusion_vreg.nii"',
        )


def _gen_fname(
    basename, cwd=None, suffix=None, change_ext=True, ext=None, output_type=None
):
    """Generate a filename based on the given parameters.

    The filename will take the form: cwd/basename<suffix><ext>.
    If change_ext is True, it will use the extensions specified in
    <instance>inputs.output_type.

    Parameters
    ----------
    basename : str
        Filename to base the new filename on.
    cwd : str
        Path to prefix to the new filename. (default is output_dir)
    suffix : str
        Suffix to add to the `basename`.  (defaults is '' )
    change_ext : bool
        Flag to change the filename extension to the FSL output type.
        (default True)

    Returns
    -------
    fname : str
        New filename based on given parameters.

    """

    if basename == "":
        msg = "Unable to generate filename for command %s. " % "vecreg"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(output_type)
    if change_ext:
        if suffix:
            suffix = f"{suffix}{ext}"
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


def _list_outputs(in_file=None, out_file=None, output_type=None):
    outputs = {}
    outputs["out_file"] = out_file
    if (outputs["out_file"] is attrs.NOTHING) and (in_file is not attrs.NOTHING):
        pth, base_name = os.path.split(in_file)
        outputs["out_file"] = _gen_fname(
            base_name, cwd=os.path.abspath(pth), suffix="_vreg", output_type=output_type
        )
    outputs["out_file"] = os.path.abspath(outputs["out_file"])
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
