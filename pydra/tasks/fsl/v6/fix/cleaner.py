import attrs
from fileformats.generic import File
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["cleaned_functional_file"] = _get_cleaned_functional_filename(
        inputs["artifacts_list_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    return outputs


def cleaned_functional_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("cleaned_functional_file")


@shell.define
class Cleaner(shell.Task["Cleaner.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.fix.cleaner import Cleaner

    """

    executable = "fix -a"
    artifacts_list_file: File = shell.arg(
        help="Text file listing which ICs are artifacts; can be the output from classification or can be created manually",
        argstr="{artifacts_list_file}",
        position=1,
    )
    cleanup_motion: bool = shell.arg(
        help="cleanup motion confounds, looks for design.fsf for highpass filter cut-off",
        argstr="-m",
        position=2,
    )
    highpass: float = shell.arg(
        help="cleanup motion confounds",
        argstr="-m -h {highpass}",
        position=3,
        default=100,
    )
    aggressive: bool = shell.arg(
        help="Apply aggressive (full variance) cleanup, instead of the default less-aggressive (unique variance) cleanup.",
        argstr="-A",
        position=4,
    )
    confound_file: File = shell.arg(
        help="Include additional confound file.",
        argstr="-x {confound_file}",
        position=5,
    )
    confound_file_1: File = shell.arg(
        help="Include additional confound file.",
        argstr="-x {confound_file_1}",
        position=6,
    )
    confound_file_2: File = shell.arg(
        help="Include additional confound file.",
        argstr="-x {confound_file_2}",
        position=7,
    )

    class Outputs(shell.Outputs):
        cleaned_functional_file: File | None = shell.out(
            help="Cleaned session data", callable=cleaned_functional_file_callable
        )


def _get_cleaned_functional_filename(
    artifacts_list_filename, inputs=None, output_dir=None, stderr=None, stdout=None
):
    """extract the proper filename from the first line of the artifacts file"""
    artifacts_list_file = open(artifacts_list_filename)
    functional_filename, extension = artifacts_list_file.readline().split(".")
    artifacts_list_file_path, artifacts_list_filename = os.path.split(
        artifacts_list_filename
    )

    return os.path.join(artifacts_list_file_path, functional_filename + "_clean.nii.gz")
