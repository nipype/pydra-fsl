from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _parse_inputs(inputs, output_dir=None):
    if not output_dir:
        output_dir = os.getcwd()
    parsed_inputs = {}
    skip = []

    if skip is None:
        skip = []
    if inputs["real_cartesian"]:
        skip += inputs["_ofs"][:3]
    elif inputs["real_polar"]:
        skip += inputs["_ofs"][:1] + inputs["_ofs"][3:]
    else:
        skip += inputs["_ofs"][1:]

    return parsed_inputs


def _gen_filename(name, inputs):
    parsed_inputs = _parse_inputs(inputs) if inputs else {}
    if name == "complex_out_file":
        if inputs["complex_cartesian"]:
            in_file = inputs["real_in_file"]
        elif inputs["complex_polar"]:
            in_file = inputs["magnitude_in_file"]
        elif inputs["complex_split"] or inputs["complex_merge"]:
            in_file = inputs["complex_in_file"]
        else:
            return None
        return _gen_fname(in_file, suffix="_cplx", output_type=inputs["output_type"])
    elif name == "magnitude_out_file":
        return _gen_fname(
            inputs["complex_in_file"], suffix="_mag", output_type=inputs["output_type"]
        )
    elif name == "phase_out_file":
        return _gen_fname(
            inputs["complex_in_file"],
            suffix="_phase",
            output_type=inputs["output_type"],
        )
    elif name == "real_out_file":
        return _gen_fname(
            inputs["complex_in_file"], suffix="_real", output_type=inputs["output_type"]
        )
    elif name == "imaginary_out_file":
        return _gen_fname(
            inputs["complex_in_file"], suffix="_imag", output_type=inputs["output_type"]
        )
    return None


def complex_out_file_default(inputs):
    return _gen_filename("complex_out_file", inputs=inputs)


def imaginary_out_file_default(inputs):
    return _gen_filename("imaginary_out_file", inputs=inputs)


def magnitude_out_file_default(inputs):
    return _gen_filename("magnitude_out_file", inputs=inputs)


def phase_out_file_default(inputs):
    return _gen_filename("phase_out_file", inputs=inputs)


def real_out_file_default(inputs):
    return _gen_filename("real_out_file", inputs=inputs)


@shell.define(
    xor=[
        [
            "complex_cartesian",
            "complex_merge",
            "complex_out_file",
            "complex_polar",
            "complex_split",
            "imaginary_out_file",
            "magnitude_out_file",
            "phase_out_file",
            "real_polar",
        ],
        [
            "complex_cartesian",
            "complex_merge",
            "complex_out_file",
            "complex_polar",
            "complex_split",
            "imaginary_out_file",
            "magnitude_out_file",
            "real_cartesian",
            "real_out_file",
        ],
        [
            "complex_cartesian",
            "complex_merge",
            "complex_out_file",
            "complex_polar",
            "complex_split",
            "imaginary_out_file",
            "phase_out_file",
            "real_cartesian",
            "real_out_file",
        ],
        [
            "complex_cartesian",
            "complex_merge",
            "complex_out_file",
            "complex_polar",
            "complex_split",
            "magnitude_out_file",
            "phase_out_file",
            "real_out_file",
            "real_polar",
        ],
        [
            "complex_cartesian",
            "complex_merge",
            "complex_polar",
            "complex_split",
            "end_vol",
            "real_cartesian",
            "real_polar",
            "start_vol",
        ],
        [
            "complex_cartesian",
            "complex_merge",
            "complex_polar",
            "complex_split",
            "real_cartesian",
            "real_polar",
        ],
        [
            "complex_out_file",
            "imaginary_out_file",
            "magnitude_out_file",
            "phase_out_file",
            "real_cartesian",
            "real_out_file",
            "real_polar",
        ],
        ["complex_in_file", "real_in_file", "magnitude_in_file"],
        ["complex_in_file2", "imaginary_in_file", "phase_in_file"],
    ]
)
class Complex(shell.Task["Complex.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.complex import Complex

    """

    executable = "fslcomplex"
    complex_in_file: File | None = shell.arg(
        help="", argstr="{complex_in_file}", position=2
    )
    complex_in_file2: File | None = shell.arg(
        help="", argstr="{complex_in_file2}", position=3
    )
    real_in_file: File | None = shell.arg(help="", argstr="{real_in_file}", position=2)
    imaginary_in_file: File | None = shell.arg(
        help="", argstr="{imaginary_in_file}", position=3
    )
    magnitude_in_file: File | None = shell.arg(
        help="", argstr="{magnitude_in_file}", position=2
    )
    phase_in_file: File | None = shell.arg(
        help="", argstr="{phase_in_file}", position=3
    )
    start_vol: int | None = shell.arg(help="", argstr="{start_vol}", position=-2)
    end_vol: int | None = shell.arg(help="", argstr="{end_vol}", position=-1)
    real_polar: bool = shell.arg(help="", argstr="-realpolar", position=1)
    real_cartesian: bool = shell.arg(help="", argstr="-realcartesian", position=1)
    complex_cartesian: bool = shell.arg(help="", argstr="-complex", position=1)
    complex_polar: bool = shell.arg(help="", argstr="-complexpolar", position=1)
    complex_split: bool = shell.arg(help="", argstr="-complexsplit", position=1)
    complex_merge: bool = shell.arg(help="", argstr="-complexmerge", position=1)

    class Outputs(shell.Outputs):
        complex_out_file: Path | None = shell.outarg(
            help="",
            argstr="{complex_out_file}",
            position=-3,
            path_template="complex_out_file",
        )
        magnitude_out_file: Path | None = shell.outarg(
            help="",
            argstr="{magnitude_out_file}",
            position=-4,
            path_template="magnitude_out_file",
        )
        phase_out_file: Path | None = shell.outarg(
            help="",
            argstr="{phase_out_file}",
            position=-3,
            path_template="phase_out_file",
        )
        real_out_file: Path | None = shell.outarg(
            help="",
            argstr="{real_out_file}",
            position=-4,
            path_template="real_out_file",
        )
        imaginary_out_file: Path | None = shell.outarg(
            help="",
            argstr="{imaginary_out_file}",
            position=-3,
            path_template="imaginary_out_file",
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
        msg = "Unable to generate filename for command %s. " % "fslcomplex"
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
