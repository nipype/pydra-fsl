import attrs
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

    if name == "plot_type":
        source = inputs["in_source"]

        if inputs["plot_type"] == "displacement":
            title = "-t 'MCFLIRT estimated mean displacement (mm)'"
            labels = "-a abs,rel"
            return f"{title} {labels}"

        sfdict = dict(fsl_rot=(1, 3), fsl_tra=(4, 6), spm_rot=(4, 6), spm_tra=(1, 3))

        sfstr = "--start=%d --finish=%d" % sfdict[f"{source}_{value[:3]}"]
        titledict = dict(fsl="MCFLIRT", spm="Realign")
        unitdict = dict(rot="radians", tra="mm")

        title = "'{} estimated {} ({})'".format(
            titledict[source],
            value,
            unitdict[value[:3]],
        )

        return f"-t {title} {sfstr} -a x,y,z"
    elif name == "plot_size":
        return "-h %d -w %d" % value
    elif name == "in_file":
        if isinstance(value, list):
            args = ",".join(value)
            return "-i %s" % args
        else:
            return "-i %s" % value

    return argstr.format(**inputs)


def plot_type_formatter(field, inputs):
    return _format_arg("plot_type", field, inputs, argstr="{plot_type}")


def plot_size_formatter(field, inputs):
    return _format_arg("plot_size", field, inputs, argstr="{plot_size}")


def in_file_formatter(field, inputs):
    return _format_arg("in_file", field, inputs, argstr="{in_file}")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            plot_type=inputs["plot_type"],
        )["out_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class PlotMotionParams(shell.Task["PlotMotionParams.Outputs"]):
    """
    Examples
    -------

    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.plot_motion_params import PlotMotionParams

    """

    executable = "fsl_tsplot"
    in_file: ty.Any = shell.arg(
        help="file with motion parameters", position=1, formatter=in_file_formatter
    )
    in_source: ty.Any = shell.arg(
        help="which program generated the motion parameter file - fsl, spm"
    )
    plot_type: ty.Any = shell.arg(
        help="which motion type to plot - rotations, translations, displacement",
        formatter=plot_type_formatter,
    )
    plot_size: ty.Any = shell.arg(
        help="plot image height and width", formatter=plot_size_formatter
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="image to write", argstr="-o {out_file}", path_template="out_file"
        )


def _list_outputs(in_file=None, out_file=None, plot_type=None):
    outputs = {}
    out_file = out_file
    if out_file is attrs.NOTHING:
        if isinstance(in_file, list):
            infile = in_file[0]
        else:
            infile = in_file
        plttype = dict(rot="rot", tra="trans", dis="disp")[plot_type[:3]]
        out_file = fname_presuffix(infile, suffix="_%s.png" % plttype, use_ext=False)
    outputs["out_file"] = os.path.abspath(out_file)
    return outputs
