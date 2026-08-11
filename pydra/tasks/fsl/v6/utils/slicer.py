import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "show_orientation":
        if value:
            return ""
        else:
            return "-u"
    elif name == "label_slices":
        if value:
            return "-L"
        else:
            return ""

    return argstr.format(**inputs)


def show_orientation_formatter(field, inputs):
    return _format_arg("show_orientation", field, inputs, argstr="{show_orientation:d}")


def label_slices_formatter(field, inputs):
    return _format_arg("label_slices", field, inputs, argstr="-L")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )["out_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(xor=[["all_axial", "middle_slices", "sample_axial", "single_slice"]])
class Slicer(shell.Task["Slicer.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.slicer import Slicer

    """

    executable = "slicer"
    in_file: File = shell.arg(help="input volume", argstr="{in_file}", position=2)
    image_edges: File = shell.arg(
        help="volume to display edge overlay for (useful for checking registration",
        argstr="{image_edges}",
        position=3,
    )
    label_slices: bool = shell.arg(
        help="display slice number",
        formatter=label_slices_formatter,
        position=4,
        default=True,
    )
    colour_map: File = shell.arg(
        help="use different colour map from that stored in nifti header",
        argstr="-l {colour_map}",
        position=5,
    )
    intensity_range: ty.Any = shell.arg(
        help="min and max intensities to display",
        argstr="-i {intensity_range[0]:.3} {intensity_range[1]:.3}",
        position=6,
    )
    threshold_edges: float = shell.arg(
        help="use threshold for edges", argstr="-e {threshold_edges:.3}", position=7
    )
    dither_edges: bool = shell.arg(
        help="produce semi-transparent (dithered) edges", argstr="-t", position=8
    )
    nearest_neighbour: bool = shell.arg(
        help="use nearest neighbor interpolation for output", argstr="-n", position=9
    )
    show_orientation: bool = shell.arg(
        help="label left-right orientation",
        formatter=show_orientation_formatter,
        position=10,
        default=True,
    )
    single_slice: ty.Any | None = shell.arg(
        help="output picture of single slice in the x, y, or z plane",
        argstr="-{single_slice}",
        requires=["slice_number"],
        position=11,
    )
    slice_number: int = shell.arg(
        help="slice number to save in picture", argstr="-{slice_number}", position=12
    )
    middle_slices: bool = shell.arg(
        help="output picture of mid-sagittal, axial, and coronal slices",
        argstr="-a",
        position=11,
    )
    all_axial: bool = shell.arg(
        help="output all axial slices into one picture",
        argstr="-A",
        requires=["image_width"],
        position=11,
    )
    sample_axial: int | None = shell.arg(
        help="output every n axial slices into one picture",
        argstr="-S {sample_axial}",
        requires=["image_width"],
        position=11,
    )
    image_width: int = shell.arg(
        help="max picture width", argstr="{image_width}", position=-2
    )
    scaling: float = shell.arg(help="image scale", argstr="-s {scaling}", position=1)

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="picture to write",
            argstr="{out_file}",
            position=-1,
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
        msg = "Unable to generate filename for command %s. " % "slicer"
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
    out_file = out_file
    if out_file is attrs.NOTHING:
        out_file = _gen_fname(in_file, ext=".png", output_type=output_type)
    outputs["out_file"] = os.path.abspath(out_file)
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
