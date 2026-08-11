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

    if name == "in_file":
        if isinstance(value, list):
            args = ",".join(value)
            return "-i %s" % args
        else:
            return "-i %s" % value
    elif name == "labels":
        if isinstance(value, list):
            args = ",".join(value)
            return "-a %s" % args
        else:
            return "-a %s" % value
    elif name == "title":
        return "-t '%s'" % value
    elif name == "plot_range":
        return "--start=%d --finish=%d" % value
    elif name == "y_range":
        return "--ymin=%d --ymax=%d" % value
    elif name == "plot_size":
        return "-h %d -w %d" % value

    return argstr.format(**inputs)


def in_file_formatter(field, inputs):
    return _format_arg("in_file", field, inputs, argstr="{in_file}")


def labels_formatter(field, inputs):
    return _format_arg("labels", field, inputs, argstr="{labels}")


def title_formatter(field, inputs):
    return _format_arg("title", field, inputs, argstr="{title}")


def plot_range_formatter(field, inputs):
    return _format_arg("plot_range", field, inputs, argstr="{plot_range}")


def y_range_formatter(field, inputs):
    return _format_arg("y_range", field, inputs, argstr="{y_range}")


def plot_size_formatter(field, inputs):
    return _format_arg("plot_size", field, inputs, argstr="{plot_size}")


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


@shell.define(
    xor=[
        ["plot_finish", "plot_range"],
        ["plot_finish", "plot_range", "plot_start"],
        ["plot_range", "plot_start"],
        ["y_max", "y_min", "y_range"],
        ["y_max", "y_range"],
        ["y_min", "y_range"],
    ]
)
class PlotTimeSeries(shell.Task["PlotTimeSeries.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.plot_time_series import PlotTimeSeries

    """

    executable = "fsl_tsplot"
    in_file: ty.Any = shell.arg(
        help="file or list of files with columns of timecourse information",
        position=1,
        formatter=in_file_formatter,
    )
    plot_start: int | None = shell.arg(
        help="first column from in-file to plot", argstr="--start={plot_start}"
    )
    plot_finish: int | None = shell.arg(
        help="final column from in-file to plot", argstr="--finish={plot_finish}"
    )
    plot_range: ty.Any | None = shell.arg(
        help="first and last columns from the in-file to plot",
        formatter=plot_range_formatter,
    )
    title: str = shell.arg(help="plot title", formatter=title_formatter)
    legend_file: File = shell.arg(help="legend file", argstr="--legend={legend_file}")
    labels: ty.Any = shell.arg(
        help="label or list of labels", formatter=labels_formatter
    )
    y_min: float | None = shell.arg(help="minimum y value", argstr="--ymin={y_min:.2}")
    y_max: float | None = shell.arg(help="maximum y value", argstr="--ymax={y_max:.2}")
    y_range: ty.Any | None = shell.arg(
        help="min and max y axis values", formatter=y_range_formatter
    )
    x_units: int = shell.arg(
        help="scaling units for x-axis (between 1 and length of in file)",
        argstr="-u {x_units}",
        default=1,
    )
    plot_size: ty.Any = shell.arg(
        help="plot image height and width", formatter=plot_size_formatter
    )
    x_precision: int = shell.arg(
        help="precision of x-axis labels", argstr="--precision={x_precision}"
    )
    sci_notation: bool = shell.arg(help="switch on scientific notation", argstr="--sci")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="image to write", argstr="-o {out_file}", path_template="out_file"
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
        msg = "Unable to generate filename for command %s. " % "fsl_tsplot"
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
        if isinstance(in_file, list):
            infile = in_file[0]
        else:
            infile = in_file
        out_file = _gen_fname(infile, ext=".png", output_type=output_type)
    outputs["out_file"] = os.path.abspath(out_file)
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
