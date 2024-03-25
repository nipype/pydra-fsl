"""Module to put any functions that are referred to in the "callables" section of DualRegression.yaml"""

import attrs
import os


def out_dir_default(inputs):
    return _gen_filename("out_dir", inputs=inputs)


def out_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_dir"]


# Original source at L2198 of <nipype-install>/interfaces/fsl/model.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    if name == "out_dir":
        return output_dir


# Original source at L2190 of <nipype-install>/interfaces/fsl/model.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    if inputs.out_dir is not attrs.NOTHING:
        outputs["out_dir"] = os.path.abspath(inputs.out_dir)
    else:
        outputs["out_dir"] = _gen_filename(
            "out_dir",
            inputs=inputs,
            stdout=stdout,
            stderr=stderr,
            output_dir=output_dir,
        )
    return outputs
