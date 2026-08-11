import attrs
from fileformats.generic import File
from glob import glob
import logging
from pydra.tasks.fsl.v6.base import Info
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    ext = Info.output_type_to_ext(inputs["output_type"])
    outbase = "vol[0-9]*"
    if inputs["out_base_name"] is not attrs.NOTHING:
        outbase = "%s[0-9]*" % inputs["out_base_name"]
    outputs["out_files"] = sorted(glob(os.path.join(os.getcwd(), outbase + ext)))
    return outputs


def out_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_files")


@shell.define
class Split(shell.Task["Split.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.utils.split import Split

    """

    executable = "fslsplit"
    in_file: File = shell.arg(help="input filename", argstr="{in_file}", position=1)
    out_base_name: str = shell.arg(
        help="outputs prefix", argstr="{out_base_name}", position=2
    )
    dimension: ty.Any = shell.arg(
        help="dimension along which the file will be split",
        argstr="-{dimension}",
        position=3,
    )

    class Outputs(shell.Outputs):
        out_files: list[File] | None = shell.out(callable=out_files_callable)
