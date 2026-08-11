import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )[name]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class ImageMeants(shell.Task["ImageMeants.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.image_meants import ImageMeants

    """

    executable = "fslmeants"
    in_file: File = shell.arg(
        help="input file for computing the average timeseries",
        argstr="-i {in_file}",
        position=1,
    )
    mask: File = shell.arg(help="input 3D mask", argstr="-m {mask}")
    spatial_coord: list[int] = shell.arg(
        help="<x y z>  requested spatial coordinate (instead of mask)",
        argstr="-c {spatial_coord}",
    )
    use_mm: bool = shell.arg(
        help="use mm instead of voxel coordinates (for -c option)", argstr="--usemm"
    )
    show_all: bool = shell.arg(
        help="show all voxel time series (within mask) instead of averaging",
        argstr="--showall",
    )
    eig: bool = shell.arg(
        help="calculate Eigenvariate(s) instead of mean (output will have 0 mean)",
        argstr="--eig",
    )
    order: int = shell.arg(
        help="select number of Eigenvariates", argstr="--order={order}", default=1
    )
    nobin: bool = shell.arg(
        help="do not binarise the mask for calculation of Eigenvariates",
        argstr="--no_bin",
    )
    transpose: bool = shell.arg(
        help="output results in transpose format (one row per voxel/mean)",
        argstr="--transpose",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="name of output text matrix",
            argstr="-o {out_file}",
            path_template="out_file",
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
        msg = "Unable to generate filename for command %s. " % "fslmeants"
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
    if outputs["out_file"] is attrs.NOTHING:
        outputs["out_file"] = _gen_fname(
            in_file, suffix="_ts", ext=".txt", change_ext=True, output_type=output_type
        )
    outputs["out_file"] = os.path.abspath(outputs["out_file"])
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
