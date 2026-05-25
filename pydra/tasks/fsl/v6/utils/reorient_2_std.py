from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
from pathlib import Path
from pathlib import Path
from pydra.compose import shell

logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _gen_fname(
            inputs["in_file"], suffix="_reoriented", output_type=inputs["output_type"]
        )
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class Reorient2Std(shell.Task["Reorient2Std.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.reorient_2_std import Reorient2Std

    """

    executable = "fslreorient2std"
    in_file: File = shell.arg(help="", argstr="{in_file}")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="", argstr="{out_file}", path_template="out_file"
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
        msg = "Unable to generate filename for command %s. " % "fslreorient2std"
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
