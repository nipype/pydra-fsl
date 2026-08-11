import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
from glob import glob
import logging
from pydra.tasks.fsl.v6.base import Info
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    ext = Info.output_type_to_ext(inputs["output_type"])
    suffix = "_slice_*" + ext
    if inputs["out_base_name"] is not attrs.NOTHING:
        fname_template = os.path.abspath(inputs["out_base_name"] + suffix)
    else:
        fname_template = fname_presuffix(
            inputs["in_file"], suffix=suffix, use_ext=False
        )

    outputs["out_files"] = sorted(glob(fname_template))

    return outputs


def out_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_files")


@shell.define
class Slice(shell.Task["Slice.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.v6.utils.slice import Slice

    >>> task = Slice()
    >>> task.in_file = Nifti1.mock("functional.nii")
    >>> task.cmdline
    'fslslice functional.nii sl'


    """

    executable = "fslslice"
    in_file: Nifti1 = shell.arg(help="input filename", argstr="{in_file}", position=1)
    out_base_name: str = shell.arg(
        help="outputs prefix", argstr="{out_base_name}", position=2
    )

    class Outputs(shell.Outputs):
        out_files: list[File] | None = shell.out(callable=out_files_callable)
