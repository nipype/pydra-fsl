"""Module to put any functions that are referred to in the "callables" section of ICA_AROMA.yaml"""

import os


def aggr_denoised_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["aggr_denoised_file"]


def nonaggr_denoised_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["nonaggr_denoised_file"]


def out_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_dir"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L151 of <nipype-install>/interfaces/fsl/aroma.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["out_dir"] = os.path.abspath(inputs.out_dir)
    out_dir = outputs["out_dir"]

    if inputs.denoise_type in ("aggr", "both"):
        outputs["aggr_denoised_file"] = os.path.join(
            out_dir, "denoised_func_data_aggr.nii.gz"
        )
    if inputs.denoise_type in ("nonaggr", "both"):
        outputs["nonaggr_denoised_file"] = os.path.join(
            out_dir, "denoised_func_data_nonaggr.nii.gz"
        )
    return outputs
