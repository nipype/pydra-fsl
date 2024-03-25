"""Module to put any functions that are referred to in the "callables" section of AccuracyTester.yaml"""

import attrs
from fileformats.generic import Directory


def output_directory_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["output_directory"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L251 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    if inputs.output_directory is not attrs.NOTHING:
        outputs["output_directory"] = Directory(
            exists=False, value=inputs.output_directory
        )
    else:
        outputs["output_directory"] = Directory(exists=False, value="accuracy_test")
    return outputs
