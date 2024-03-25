"""Module to put any functions that are referred to in the "callables" section of L2Model.yaml"""

import os


def design_con_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["design_con"]


def design_grp_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["design_grp"]


def design_mat_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["design_mat"]


# Original source at L1431 of <nipype-install>/interfaces/fsl/model.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    for field in list(outputs.keys()):
        outputs[field] = os.path.join(output_dir, field.replace("_", "."))
    return outputs
