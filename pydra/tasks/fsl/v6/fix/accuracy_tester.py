import attrs
from fileformats.generic import Directory, File
import logging
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["output_directory"] is not attrs.NOTHING:
        outputs["output_directory"] = Directory(
            exists=False, value=inputs["output_directory"]
        )
    else:
        outputs["output_directory"] = Directory(exists=False, value="accuracy_test")
    return outputs


def output_directory_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("output_directory")


@shell.define
class AccuracyTester(shell.Task["AccuracyTester.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.v6.fix.accuracy_tester import AccuracyTester

    """

    executable = "fix -C"
    mel_icas: list[Directory] = shell.arg(
        help="Melodic output directories", argstr="{mel_icas}", position=3
    )
    trained_wts_file: File = shell.arg(
        help="trained-weights file", argstr="{trained_wts_file}", position=1
    )
    output_directory: ty.Any = shell.arg(
        help="Path to folder in which to store the results of the accuracy test.",
        argstr="{output_directory}",
        position=2,
    )

    class Outputs(shell.Outputs):
        output_directory: Directory | None = shell.out(
            help="Path to folder in which to store the results of the accuracy test.",
            callable=output_directory_callable,
        )
