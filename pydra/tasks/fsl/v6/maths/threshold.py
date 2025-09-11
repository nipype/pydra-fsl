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
    self_dict = {}

    if name == "thresh":
        arg = "-"
        _si = self_dict["inputs"]
        if inputs["direction"] == "above":
            arg += "u"
        arg += "thr"
        if (_si.use_robust_range is not attrs.NOTHING) and _si.use_robust_range:
            if (_si.use_nonzero_voxels is not attrs.NOTHING) and _si.use_nonzero_voxels:
                arg += "P"
            else:
                arg += "p"
        arg += " %.10f" % value
        return arg

    return argstr.format(**inputs)


def thresh_formatter(field, inputs):
    return _format_arg("thresh", field, inputs, argstr="{thresh}")


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


@shell.define
class Threshold(shell.Task["Threshold.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.maths.threshold import Threshold

    """

    executable = "fslmaths"
    thresh: float = shell.arg(
        help="threshold value", position=4, formatter=thresh_formatter
    )
    direction: ty.Any = shell.arg(
        help="zero-out either below or above thresh value", default="below"
    )
    use_robust_range: bool = shell.arg(
        help="interpret thresh as percentage (0-100) of robust range"
    )
    use_nonzero_voxels: bool = shell.arg(
        help="use nonzero voxels to calculate robust range",
        requires=["use_robust_range"],
        default=False,
    )
    in_file: File = shell.arg(
        help="image to operate on", argstr="{in_file}", position=2
    )
    internal_datatype: str | None = shell.arg(
        help="datatype to use for calculations (default is float)",
        argstr="-dt {internal_datatype}",
        position=1,
        default=None,
    )
    output_datatype: str | None = shell.arg(
        help="datatype to use for output (default uses input type)",
        argstr="-odt {output_datatype}",
        position=-1,
        default=None,
    )
    nan2zeros: bool = shell.arg(
        help="change NaNs to zeros before doing anything",
        argstr="-nan",
        position=3,
        default=False,
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="image to write",
            argstr="{out_file}",
            position=-2,
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
        msg = "Unable to generate filename for command %s. " % "fslmaths"
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
    self_dict = {}
    outputs = {}
    outputs["out_file"] = out_file
    if out_file is attrs.NOTHING:
        outputs["out_file"] = _gen_fname(
            in_file, suffix=self_dict["_suffix"], output_type=output_type
        )
    outputs["out_file"] = os.path.abspath(outputs["out_file"])
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
