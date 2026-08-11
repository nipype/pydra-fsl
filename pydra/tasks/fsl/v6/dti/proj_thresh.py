import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_files"] = []
    for name in inputs["in_files"]:
        cwd, base_name = os.path.split(name)
        outputs["out_files"].append(
            _gen_fname(
                base_name,
                cwd=cwd,
                suffix=f"_proj_seg_thr_{inputs['threshold']}",
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        )
    return outputs


def out_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_files")


@shell.define
class ProjThresh(shell.Task["ProjThresh.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.dti.proj_thresh import ProjThresh

    >>> task = ProjThresh()
    >>> task.in_files = ldir
    >>> task.threshold = 3
    >>> task.cmdline
    'proj_thresh seeds_to_M1.nii seeds_to_M2.nii 3'


    """

    executable = "proj_thresh"
    in_files: list[File] = shell.arg(
        help="a list of input volumes", argstr="{in_files}", position=1
    )
    threshold: int = shell.arg(
        help="threshold indicating minimum number of seed voxels entering this mask region",
        argstr="{threshold}",
        position=2,
    )

    class Outputs(shell.Outputs):
        out_files: list[File] | None = shell.out(
            help="path/name of output volume after thresholding",
            callable=out_files_callable,
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
        msg = "Unable to generate filename for command %s. " % "proj_thresh"
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
