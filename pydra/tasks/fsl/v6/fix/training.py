import attrs
from fileformats.generic import Directory, File
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["trained_wts_filestem"] is not attrs.NOTHING:
        outputs["trained_wts_file"] = os.path.abspath(
            inputs["trained_wts_filestem"] + ".RData"
        )
    else:
        outputs["trained_wts_file"] = os.path.abspath("trained_wts_file.RData")
    return outputs


def trained_wts_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("trained_wts_file")


@shell.define
class Training(shell.Task["Training.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.v6.fix.training import Training

    """

    executable = "fix -t"
    mel_icas: list[Directory] = shell.arg(
        help="Melodic output directories", argstr="{mel_icas}", position=-1
    )
    trained_wts_filestem: str = shell.arg(
        help="trained-weights filestem, used for trained_wts_file and output directories",
        argstr="{trained_wts_filestem}",
        position=1,
    )
    loo: bool = shell.arg(
        help="full leave-one-out test with classifier training", argstr="-l", position=2
    )

    class Outputs(shell.Outputs):
        trained_wts_file: File | None = shell.out(
            help="Trained-weights file", callable=trained_wts_file_callable
        )
