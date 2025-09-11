from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
import os
import os.path as op
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import tempfile


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    parsed_inputs = _parse_inputs(inputs) if inputs else {}
    if value is None:
        return ""

    if name == "out_file":
        return ""

    return argstr.format(**inputs)


def out_file_formatter(field, inputs):
    return _format_arg("out_file", field, inputs, argstr="")


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []

    fname, ext = op.splitext(inputs["in_coords"])
    parsed_inputs["_in_file"] = fname
    parsed_inputs["_outformat"] = ext[1:]
    first_args = {}

    second_args = fname + ".txt"

    if ext in [".vtk", ".trk"]:
        if parsed_inputs["_tmpfile"] is None:
            parsed_inputs["_tmpfile"] = tempfile.NamedTemporaryFile(
                suffix=".txt", dir=os.getcwd(), delete=False
            ).name
        second_args = parsed_inputs["_tmpfile"]
    return parsed_inputs


@shell.define(xor=[["coord_mm", "coord_vox"], ["warp_file", "xfm_file"]])
class WarpPointsToStd(shell.Task["WarpPointsToStd.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.warp_points_to_std import WarpPointsToStd

    >>> task = WarpPointsToStd()
    >>> task.img_file = File.mock()
    >>> task.std_file = Nifti1.mock("mni.nii")
    >>> task.premat_file = File.mock()
    >>> task.in_coords = TextFile.mock("surf.txt")
    >>> task.xfm_file = File.mock()
    >>> task.warp_file = File.mock()
    >>> task.coord_mm = True
    >>> task.cmdline
    'img2stdcoord -mm -img T1.nii -std mni.nii -warp warpfield.nii surf.txt'


    """

    executable = "img2stdcoord"
    img_file: File = shell.arg(help="filename of input image", argstr="-img {img_file}")
    std_file: Nifti1 = shell.arg(
        help="filename of destination image", argstr="-std {std_file}"
    )
    premat_file: File = shell.arg(
        help="filename of pre-warp affine transform (e.g. example_func2highres.mat)",
        argstr="-premat {premat_file}",
    )
    in_coords: TextFile = shell.arg(
        help="filename of file containing coordinates",
        argstr="{in_coords}",
        position=-1,
    )
    xfm_file: File | None = shell.arg(
        help="filename of affine transform (e.g. source2dest.mat)",
        argstr="-xfm {xfm_file}",
    )
    warp_file: File | None = shell.arg(
        help="filename of warpfield (e.g. intermediate2dest_warp.nii.gz)",
        argstr="-warp {warp_file}",
    )
    coord_vox: bool = shell.arg(
        help="all coordinates in voxels - default", argstr="-vox"
    )
    coord_mm: bool = shell.arg(help="all coordinates in mm", argstr="-mm")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output file name",
            path_template="{in_coords}_warped",
            formatter=out_file_formatter,
        )
