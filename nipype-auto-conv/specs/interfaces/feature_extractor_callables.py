"""Module to put any functions that are referred to in the "callables" section of FeatureExtractor.yaml"""


def mel_ica_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["mel_ica"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L161 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["mel_ica"] = inputs.mel_ica
    return outputs
