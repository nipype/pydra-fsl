import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import numpy as np
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "filter_columns":
        return argstr.format(**{name: ",".join(map(str, value))})
    elif name == "filter_all":
        design = np.loadtxt(inputs["design_file"])
        try:
            n_cols = design.shape[1]
        except IndexError:
            n_cols = 1
        return argstr.format(**{name: ",".join(map(str, list(range(1, n_cols + 1))))})

    return argstr.format(**inputs)


def filter_columns_formatter(field, inputs):
    return _format_arg("filter_columns", field, inputs, argstr="-f '{filter_columns}'")


def filter_all_formatter(field, inputs):
    return _format_arg("filter_all", field, inputs, argstr="-f '{filter_all:d}'")


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


@shell.define(xor=[["filter_all", "filter_columns"]])
class FilterRegressor(shell.Task["FilterRegressor.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.filter_regressor import FilterRegressor

    """

    executable = "fsl_regfilt"
    in_file: File = shell.arg(
        help="input file name (4D image)", argstr="-i {in_file}", position=1
    )
    design_file: File = shell.arg(
        help="name of the matrix with time courses (e.g. GLM design or MELODIC mixing matrix)",
        argstr="-d {design_file}",
        position=3,
    )
    filter_columns: list[int] = shell.arg(
        help="(1-based) column indices to filter out of the data",
        position=4,
        formatter=filter_columns_formatter,
    )
    filter_all: bool = shell.arg(
        help="use all columns in the design file in denoising",
        position=4,
        formatter=filter_all_formatter,
    )
    mask: File = shell.arg(help="mask image file name", argstr="-m {mask}")
    var_norm: bool = shell.arg(
        help="perform variance-normalization on data", argstr="--vn"
    )
    out_vnscales: bool = shell.arg(
        help="output scaling factors for variance normalization",
        argstr="--out_vnscales",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output file name for the filtered data",
            argstr="-o {out_file}",
            position=2,
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
        msg = "Unable to generate filename for command %s. " % "fsl_regfilt"
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
            in_file, suffix="_regfilt", output_type=output_type
        )
    outputs["out_file"] = os.path.abspath(outputs["out_file"])
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
