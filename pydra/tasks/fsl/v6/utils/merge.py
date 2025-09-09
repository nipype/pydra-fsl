import attrs
from fileformats.medimage import Nifti1
import logging
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "tr":
        if inputs["dimension"] != "t":
            raise ValueError("When TR is specified, dimension must be t")
        return argstr.format(**{name: value})
    if name == "dimension":
        if inputs["tr"] is not attrs.NOTHING:
            return "-tr"
        return argstr.format(**{name: value})

    return argstr.format(**inputs)


def tr_formatter(field, inputs):
    return _format_arg("tr", field, inputs, argstr="{tr:.2}")


def dimension_formatter(field, inputs):
    return _format_arg("dimension", field, inputs, argstr="-{dimension}")


@shell.define
class Merge(shell.Task["Merge.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.utils.merge import Merge

    >>> task = Merge()
    >>> task.in_files = [Nifti1.mock("functional2.nii"), Nifti1.mock("functional3.nii")]
    >>> task.tr = 2.25
    >>> task.cmdline
    'fslmerge -tr functional2_merged.nii.gz functional2.nii functional3.nii 2.25'


    """

    executable = "fslmerge"
    in_files: list[Nifti1] = shell.arg(help="", argstr="{in_files}", position=3)
    dimension: ty.Any = shell.arg(
        help="dimension along which to merge, optionally set tr input when dimension is t",
        formatter=dimension_formatter,
        position=1,
    )
    tr: float = shell.arg(
        help="use to specify TR in seconds (default is 1.00 sec), overrides dimension and sets it to tr",
        position=-1,
        formatter=tr_formatter,
    )

    class Outputs(shell.Outputs):
        merged_file: Path = shell.outarg(
            help="",
            argstr="{merged_file}",
            path_template="{in_files}_merged",
            position=2,
        )
