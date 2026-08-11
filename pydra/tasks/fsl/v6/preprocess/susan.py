import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import numpy as np
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "fwhm":
        return argstr % (float(value) / np.sqrt(8 * np.log(2)))
    if name == "usans":
        if not value:
            return "0"
        arglist = [str(len(value))]
        for filename, thresh in value:
            arglist.extend([filename, "%.10f" % thresh])
        return " ".join(arglist)

    return argstr.format(**inputs)


def fwhm_formatter(field, inputs):
    return _format_arg("fwhm", field, inputs, argstr="{fwhm:.10}")


def usans_formatter(field, inputs):
    return _format_arg("usans", field, inputs, argstr="")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    out_file = inputs["out_file"]
    if out_file is attrs.NOTHING:
        out_file = _gen_fname(
            inputs["in_file"],
            suffix="_smooth",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    outputs["smoothed_file"] = os.path.abspath(out_file)
    return outputs


def smoothed_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("smoothed_file")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )["smoothed_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class SUSAN(shell.Task["SUSAN.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.susan import SUSAN

    """

    executable = "susan"
    in_file: File = shell.arg(
        help="filename of input timeseries", argstr="{in_file}", position=1
    )
    brightness_threshold: float = shell.arg(
        help="brightness threshold and should be greater than noise level and less than contrast of edges to be preserved.",
        argstr="{brightness_threshold:.10}",
        position=2,
    )
    fwhm: float = shell.arg(
        help="fwhm of smoothing, in mm, gets converted using sqrt(8*log(2))",
        position=3,
        formatter=fwhm_formatter,
    )
    dimension: ty.Any = shell.arg(
        help="within-plane (2) or fully 3D (3)",
        argstr="{dimension}",
        position=4,
        default=3,
    )
    use_median: ty.Any = shell.arg(
        help="whether to use a local median filter in the cases where single-point noise is detected",
        argstr="{use_median}",
        position=5,
        default=1,
    )
    usans: list[ty.Any] = shell.arg(
        help="determines whether the smoothing area (USAN) is to be found from secondary images (0, 1 or 2). A negative value for any brightness threshold will auto-set the threshold at 10% of the robust range",
        position=6,
        formatter=usans_formatter,
        default=[],
    )
    out_file: Path = shell.arg(
        help="output file name", argstr="{out_file}", position=-1
    )

    class Outputs(shell.Outputs):
        smoothed_file: File | None = shell.out(
            help="smoothed output file", callable=smoothed_file_callable
        )


def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
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
        msg = "Unable to generate filename for command %s. " % "susan"
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


IFLOGGER = logging.getLogger("nipype.interface")
