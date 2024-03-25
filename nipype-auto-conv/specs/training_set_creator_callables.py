"""Module to put any functions that are referred to in the "callables" section of TrainingSetCreator.yaml"""

import os


def mel_icas_out_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["mel_icas_out"]


# Original source at L122 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    mel_icas = []
    for item in inputs.mel_icas_in:
        if os.path.exists(os.path.join(item, "hand_labels_noise.txt")):
            mel_icas.append(item)
    outputs = {}
    outputs["mel_icas_out"] = mel_icas
    return outputs
