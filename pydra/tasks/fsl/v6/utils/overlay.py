import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import (
    fname_presuffix,
    split_filename,
)
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "transparency":
        if value:
            return "1"
        else:
            return "0"
    if name == "out_type":
        if value == "float":
            return "0"
        else:
            return "1"
    if name == "show_negative_stats":
        return "{} {:.2f} {:.2f}".format(
            inputs["stat_image"],
            inputs["stat_thresh"][0] * -1,
            inputs["stat_thresh"][1] * -1,
        )

    return argstr.format(**inputs)


def transparency_formatter(field, inputs):
    return _format_arg("transparency", field, inputs, argstr="{transparency:d}")


def out_type_formatter(field, inputs):
    return _format_arg("out_type", field, inputs, argstr="{out_type}")


def show_negative_stats_formatter(field, inputs):
    return _format_arg(
        "show_negative_stats", field, inputs, argstr="{show_negative_stats:d}"
    )


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
            show_negative_stats=inputs["show_negative_stats"],
            stat_image=inputs["stat_image"],
            stat_image2=inputs["stat_image2"],
        )["out_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define(
    xor=[
        ["auto_thresh_bg", "bg_thresh", "full_bg_range"],
        ["show_negative_stats", "stat_image2"],
    ]
)
class Overlay(shell.Task["Overlay.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.overlay import Overlay

    """

    executable = "overlay"
    transparency: bool = shell.arg(
        help="make overlay colors semi-transparent",
        position=1,
        formatter=transparency_formatter,
        default=True,
    )
    out_type: ty.Any = shell.arg(
        help="write output with float or int",
        position=2,
        formatter=out_type_formatter,
        default="float",
    )
    use_checkerboard: bool = shell.arg(
        help="use checkerboard mask for overlay", argstr="-c", position=3
    )
    background_image: File = shell.arg(
        help="image to use as background", argstr="{background_image}", position=4
    )
    auto_thresh_bg: bool = shell.arg(
        help="automatically threshold the background image", argstr="-a", position=5
    )
    full_bg_range: bool = shell.arg(
        help="use full range of background image", argstr="-A", position=5
    )
    bg_thresh: ty.Any | None = shell.arg(
        help="min and max values for background intensity",
        argstr="{bg_thresh[0]:.3} {bg_thresh[1]:.3}",
        position=5,
    )
    stat_image: File = shell.arg(
        help="statistical image to overlay in color", argstr="{stat_image}", position=6
    )
    stat_thresh: ty.Any = shell.arg(
        help="min and max values for the statistical overlay",
        argstr="{stat_thresh[0]:.2} {stat_thresh[1]:.2}",
        position=7,
    )
    show_negative_stats: bool = shell.arg(
        help="display negative statistics in overlay",
        position=8,
        formatter=show_negative_stats_formatter,
    )
    stat_image2: File | None = shell.arg(
        help="second statistical image to overlay in color",
        argstr="{stat_image2}",
        position=9,
    )
    stat_thresh2: ty.Any = shell.arg(
        help="min and max values for second statistical overlay",
        argstr="{stat_thresh2[0]:.2} {stat_thresh2[1]:.2}",
        position=10,
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="combined image volume",
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
        msg = "Unable to generate filename for command %s. " % "overlay"
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


def _list_outputs(
    out_file=None,
    output_type=None,
    show_negative_stats=None,
    stat_image=None,
    stat_image2=None,
):
    outputs = {}
    out_file = out_file
    if out_file is attrs.NOTHING:
        if (stat_image2 is not attrs.NOTHING) and (
            (show_negative_stats is attrs.NOTHING) or not show_negative_stats
        ):
            stem = "{}_and_{}".format(
                split_filename(stat_image)[1],
                split_filename(stat_image2)[1],
            )
        else:
            stem = split_filename(stat_image)[1]
        out_file = _gen_fname(stem, suffix="_overlay", output_type=output_type)
    outputs["out_file"] = os.path.abspath(out_file)
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
