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


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    out_file = inputs["out_file"]
    if out_file is attrs.NOTHING:
        out_file = _gen_fname(
            inputs["in_file"],
            suffix="_st",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    outputs["slice_time_corrected_file"] = os.path.abspath(out_file)
    return outputs


def slice_time_corrected_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("slice_time_corrected_file")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )["slice_time_corrected_file"]
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class SliceTimer(shell.Task["SliceTimer.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.slice_timer import SliceTimer

    """

    executable = "slicetimer"
    in_file: File = shell.arg(
        help="filename of input timeseries", argstr="--in={in_file}", position=1
    )
    out_file: Path = shell.arg(
        help="filename of output timeseries", argstr="--out={out_file}"
    )
    index_dir: bool = shell.arg(
        help="slice indexing from top to bottom", argstr="--down"
    )
    time_repetition: float = shell.arg(
        help="Specify TR of data - default is 3s", argstr="--repeat={time_repetition}"
    )
    slice_direction: ty.Any = shell.arg(
        help="direction of slice acquisition (x=1, y=2, z=3) - default is z",
        argstr="--direction={slice_direction}",
    )
    interleaved: bool = shell.arg(help="use interleaved acquisition", argstr="--odd")
    custom_timings: File = shell.arg(
        help="slice timings, in fractions of TR, range 0:1 (default is 0.5 = no shift)",
        argstr="--tcustom={custom_timings}",
    )
    global_shift: float = shell.arg(
        help="shift in fraction of TR, range 0:1 (default is 0.5 = no shift)",
        argstr="--tglobal",
    )
    custom_order: File = shell.arg(
        help="filename of single-column custom interleave order file (first slice is referred to as 1 not 0)",
        argstr="--ocustom={custom_order}",
    )

    class Outputs(shell.Outputs):
        slice_time_corrected_file: File | None = shell.out(
            help="slice time corrected file",
            callable=slice_time_corrected_file_callable,
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
        msg = "Unable to generate filename for command %s. " % "slicetimer"
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
