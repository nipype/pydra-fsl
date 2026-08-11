import attrs
from fileformats.generic import Directory, File
from glob import glob
import logging
import os
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    is_ica = False
    outputs["feat_dir"] = None
    with open(inputs["fsf_file"]) as fp:
        text = fp.read()
        if "set fmri(inmelodic) 1" in text:
            is_ica = True
        for line in text.split("\n"):
            if line.find("set fmri(outputdir)") > -1:
                try:
                    outputdir_spec = line.split('"')[-2]
                    if os.path.exists(outputdir_spec):
                        outputs["feat_dir"] = outputdir_spec

                except:
                    pass
    if not outputs["feat_dir"]:
        if is_ica:
            outputs["feat_dir"] = glob(os.path.join(os.getcwd(), "*ica"))[0]
        else:
            outputs["feat_dir"] = glob(os.path.join(os.getcwd(), "*feat"))[0]
    return outputs


def feat_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("feat_dir")


@shell.define
class FEAT(shell.Task["FEAT.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.v6.model.feat import FEAT

    """

    executable = "feat"
    fsf_file: File = shell.arg(
        help="File specifying the feat design spec file",
        argstr="{fsf_file}",
        position=1,
    )

    class Outputs(shell.Outputs):
        feat_dir: Directory | None = shell.out(callable=feat_dir_callable)
