"""Module to put any functions that are referred to in the "callables" section of FEAT.yaml"""

import os
from glob import glob


def feat_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["feat_dir"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L465 of <nipype-install>/interfaces/fsl/model.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    is_ica = False
    outputs["feat_dir"] = None
    with open(inputs.fsf_file, "rt") as fp:
        text = fp.read()
        if "set fmri(inmelodic) 1" in text:
            is_ica = True
        for line in text.split("\n"):
            if line.find("set fmri(outputdir)") > -1:
                try:
                    outputdir_spec = line.split('"')[-2]
                    if os.path.exists(outputdir_spec):
                        outputs["feat_dir"] = outputdir_spec

                except:
                    pass
    if not outputs["feat_dir"]:
        if is_ica:
            outputs["feat_dir"] = glob(os.path.join(output_dir, "*ica"))[0]
        else:
            outputs["feat_dir"] = glob(os.path.join(output_dir, "*feat"))[0]
    return outputs
