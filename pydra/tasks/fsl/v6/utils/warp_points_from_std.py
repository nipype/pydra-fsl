import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
import os.path as op
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = op.abspath("stdout.nipype")
    return outputs


def out_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_file")


@shell.define(xor=[["coord_mm", "coord_vox"], ["warp_file", "xfm_file"]])
class WarpPointsFromStd(shell.Task["WarpPointsFromStd.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from fileformats.text import TextFile
    >>> from pydra.tasks.fsl.v6.utils.warp_points_from_std import WarpPointsFromStd

    >>> task = WarpPointsFromStd()
    >>> task.img_file = File.mock()
    >>> task.std_file = Nifti1.mock("mni.nii")
    >>> task.in_coords = TextFile.mock("surf.txt")
    >>> task.xfm_file = File.mock()
    >>> task.warp_file = File.mock()
    >>> task.coord_mm = True
    >>> task.cmdline
    'std2imgcoord -mm -img T1.nii -std mni.nii -warp warpfield.nii surf.txt'


    """

    executable = "std2imgcoord"
    img_file: File = shell.arg(
        help="filename of a destination image", argstr="-img {img_file}"
    )
    std_file: Nifti1 = shell.arg(
        help="filename of the image in standard space", argstr="-std {std_file}"
    )
    in_coords: TextFile = shell.arg(
        help="filename of file containing coordinates",
        argstr="{in_coords}",
        position=-2,
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
        out_file: File | None = shell.out(
            help="Name of output file, containing the warp as field or coefficients.",
            callable=out_file_callable,
        )
