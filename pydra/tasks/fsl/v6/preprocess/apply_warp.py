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

    if name == "superlevel":
        return argstr.format(**{name: str(value)})

    return argstr.format(**inputs)


def superlevel_formatter(field, inputs):
    return _format_arg("superlevel", field, inputs, argstr="--superlevel={superlevel}")


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


@shell.define(xor=[["abswarp", "relwarp"]])
class ApplyWarp(shell.Task["ApplyWarp.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.apply_warp import ApplyWarp

    """

    executable = "applywarp"
    in_file: File = shell.arg(
        help="image to be warped", argstr="--in={in_file}", position=1
    )
    ref_file: File = shell.arg(
        help="reference image", argstr="--ref={ref_file}", position=2
    )
    field_file: File = shell.arg(
        help="file containing warp field", argstr="--warp={field_file}"
    )
    abswarp: bool = shell.arg(
        help="treat warp field as absolute: x' = w(x)", argstr="--abs"
    )
    relwarp: bool = shell.arg(
        help="treat warp field as relative: x' = x + w(x)", argstr="--rel", position=-1
    )
    datatype: ty.Any = shell.arg(
        help="Force output data type [char short int float double].",
        argstr="--datatype={datatype}",
    )
    supersample: bool = shell.arg(
        help="intermediary supersampling of output, default is off", argstr="--super"
    )
    superlevel: ty.Any = shell.arg(
        help="level of intermediary supersampling, a for 'automatic' or integer level. Default = 2",
        formatter=superlevel_formatter,
    )
    premat: File = shell.arg(
        help="filename for pre-transform (affine matrix)", argstr="--premat={premat}"
    )
    postmat: File = shell.arg(
        help="filename for post-transform (affine matrix)", argstr="--postmat={postmat}"
    )
    mask_file: File = shell.arg(
        help="filename for mask image (in reference space)", argstr="--mask={mask_file}"
    )
    interp: ty.Any = shell.arg(
        help="interpolation method", argstr="--interp={interp}", position=-2
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="output filename",
            argstr="--out={out_file}",
            path_template="out_file",
            position=3,
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
        msg = "Unable to generate filename for command %s. " % "applywarp"
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
    if out_file is attrs.NOTHING:
        outputs["out_file"] = _gen_fname(
            in_file, suffix="_warp", output_type=output_type
        )
    else:
        outputs["out_file"] = os.path.abspath(out_file)
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
