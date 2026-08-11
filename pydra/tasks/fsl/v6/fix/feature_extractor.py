import attrs
from fileformats.generic import Directory
import logging
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["mel_ica"] = inputs["mel_ica"]
    return outputs


def mel_ica_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mel_ica")


@shell.define
class FeatureExtractor(shell.Task["FeatureExtractor.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pydra.tasks.fsl.v6.fix.feature_extractor import FeatureExtractor

    """

    executable = "fix -f"
    mel_ica: ty.Any = shell.arg(
        help="Melodic output directory or directories", argstr="{mel_ica}", position=-1
    )

    class Outputs(shell.Outputs):
        mel_ica: Directory | None = shell.out(
            help="Melodic output directory or directories", callable=mel_ica_callable
        )
