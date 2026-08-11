import attrs
from fileformats.generic import Directory, File
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["artifacts_list_file"] = _gen_artifacts_list_file(
        inputs["mel_ica"],
        inputs["thresh"],
        trained_wts_file=inputs["trained_wts_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )

    return outputs


def artifacts_list_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("artifacts_list_file")


@shell.define
class Classifier(shell.Task["Classifier.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.fix.classifier import Classifier

    """

    executable = "fix -c"
    mel_ica: Directory = shell.arg(
        help="Melodic output directory or directories", argstr="{mel_ica}", position=1
    )
    trained_wts_file: File = shell.arg(
        help="trained-weights file", argstr="{trained_wts_file}", position=2
    )
    thresh: int = shell.arg(
        help="Threshold for cleanup.", argstr="{thresh}", position=-1
    )
    artifacts_list_file: Path = shell.arg(
        help="Text file listing which ICs are artifacts; can be the output from classification or can be created manually"
    )

    class Outputs(shell.Outputs):
        artifacts_list_file: File | None = shell.out(
            help="Text file listing which ICs are artifacts; can be the output from classification or can be created manually",
            callable=artifacts_list_file_callable,
        )


def _gen_artifacts_list_file(
    mel_ica,
    thresh,
    trained_wts_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    _, trained_wts_file = os.path.split(trained_wts_file)
    trained_wts_filestem = trained_wts_file.split(".")[0]
    filestem = "fix4melview_" + trained_wts_filestem + "_thr"

    fname = os.path.join(mel_ica, filestem + str(thresh) + ".txt")
    return fname
