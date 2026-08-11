import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _gen_filename(name, inputs):
    if name == "out_file":
        return _list_outputs(
            out_file=inputs["out_file"], output_type=inputs["output_type"]
        )[name]
    else:
        return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class FindTheBiggest(shell.Task["FindTheBiggest.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.dti.find_the_biggest import FindTheBiggest

    >>> task = FindTheBiggest()
    >>> task.in_files = ldir
    >>> task.out_file = "biggestSegmentation"
    >>> task.cmdline
    'find_the_biggest seeds_to_M1.nii seeds_to_M2.nii biggestSegmentation'


    """

    executable = "find_the_biggest"
    in_files: list[File] = shell.arg(
        help="a list of input volumes or a singleMatrixFile",
        argstr="{in_files}",
        position=1,
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="file with the resulting segmentation",
            argstr="{out_file}",
            path_template='"biggestSegmentation"',
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
        msg = "Unable to generate filename for command %s. " % "find_the_biggest"
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


def _list_outputs(out_file=None, output_type=None):
    outputs = {}
    outputs["out_file"] = out_file
    if outputs["out_file"] is attrs.NOTHING:
        outputs["out_file"] = _gen_fname(
            "biggestSegmentation", suffix="", output_type=output_type
        )
    outputs["out_file"] = os.path.abspath(outputs["out_file"])
    return outputs


IFLOGGER = logging.getLogger("nipype.interface")
