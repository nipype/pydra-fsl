"""Module to put any functions that are referred to in the "callables" section of Classifier.yaml"""

import os


def artifacts_list_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["artifacts_list_file"]


# Original source at L304 of <nipype-install>/interfaces/fsl/fix.py
def _gen_artifacts_list_file(
    mel_ica, thresh, inputs=None, stdout=None, stderr=None, output_dir=None
):
    _, trained_wts_file = os.path.split(inputs.trained_wts_file)
    trained_wts_filestem = trained_wts_file.split(".")[0]
    filestem = "fix4melview_" + trained_wts_filestem + "_thr"

    fname = os.path.join(mel_ica, filestem + str(thresh) + ".txt")
    return fname


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L312 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["artifacts_list_file"] = _gen_artifacts_list_file(
        inputs.mel_ica,
        inputs.thresh,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )

    return outputs
