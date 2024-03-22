"""Module to put any functions that are referred to in the "callables" section of Cleaner.yaml"""

import os


def cleaned_functional_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["cleaned_functional_file"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L376 of <nipype-install>/interfaces/fsl/fix.py
def _get_cleaned_functional_filename(
    artifacts_list_filename, inputs=None, stdout=None, stderr=None, output_dir=None
):
    """extract the proper filename from the first line of the artifacts file"""
    artifacts_list_file = open(artifacts_list_filename, "r")
    functional_filename, extension = artifacts_list_file.readline().split(".")
    artifacts_list_file_path, artifacts_list_filename = os.path.split(
        artifacts_list_filename
    )

    return os.path.join(artifacts_list_file_path, functional_filename + "_clean.nii.gz")


# Original source at L388 of <nipype-install>/interfaces/fsl/fix.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["cleaned_functional_file"] = _get_cleaned_functional_filename(
        inputs.artifacts_list_file,
        inputs=inputs,
        stdout=stdout,
        stderr=stderr,
        output_dir=output_dir,
    )
    return outputs
