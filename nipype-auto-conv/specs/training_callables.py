"""Module to put any functions that are referred to in the "callables" section of Training.yaml"""

import attrs
import os


def trained_wts_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["trained_wts_file"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L200 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    if inputs.trained_wts_filestem is not attrs.NOTHING:
        outputs["trained_wts_file"] = os.path.abspath(
            inputs.trained_wts_filestem + ".RData"
        )
    else:
        outputs["trained_wts_file"] = os.path.abspath("trained_wts_file.RData")
    return outputs
