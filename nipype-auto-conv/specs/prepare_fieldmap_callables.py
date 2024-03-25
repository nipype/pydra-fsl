"""Module to put any functions that are referred to in the "callables" section of PrepareFieldmap.yaml"""


def out_fieldmap_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_fieldmap"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L110 of <nipype-install>/interfaces/fsl/epi.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["out_fieldmap"] = inputs.out_fieldmap
    return outputs
