"""Module to put any functions that are referred to in the "callables" section of EddyQuad.yaml"""

import attrs
import os
from glob import glob


def avg_b0_pe_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["avg_b0_pe_png"]


def avg_b_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["avg_b_png"]


def clean_volumes_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["clean_volumes"]


def cnr_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["cnr_png"]


def qc_json_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["qc_json"]


def qc_pdf_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["qc_pdf"]


def residuals_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["residuals"]


def vdm_png_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["vdm_png"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L1673 of <nipype-install>/interfaces/fsl/epi.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    from glob import glob

    outputs = {}

    # If the output directory isn't defined, the interface seems to use
    # the default but not set its value in `inputs.output_dir`
    if inputs.output_dir is attrs.NOTHING:
        out_dir = os.path.abspath(os.path.basename(inputs.base_name) + ".qc")
    else:
        out_dir = os.path.abspath(inputs.output_dir)

    outputs["qc_json"] = os.path.join(out_dir, "qc.json")
    outputs["qc_pdf"] = os.path.join(out_dir, "qc.pdf")

    # Grab all b* files here. This will also grab the b0_pe* files
    # as well, but only if the field input was provided. So we'll remove
    # them later in the next conditional.
    outputs["avg_b_png"] = sorted(glob(os.path.join(out_dir, "avg_b*.png")))

    if inputs.field is not attrs.NOTHING:
        outputs["avg_b0_pe_png"] = sorted(glob(os.path.join(out_dir, "avg_b0_pe*.png")))

        # The previous glob for `avg_b_png` also grabbed the
        # `avg_b0_pe_png` files so we have to remove them
        # from `avg_b_png`.
        for fname in outputs["avg_b0_pe_png"]:
            outputs["avg_b_png"].remove(fname)

        outputs["vdm_png"] = os.path.join(out_dir, "vdm.png")

    outputs["cnr_png"] = sorted(glob(os.path.join(out_dir, "cnr*.png")))

    residuals = os.path.join(out_dir, "eddy_msr.txt")
    if os.path.isfile(residuals):
        outputs["residuals"] = residuals

    clean_volumes = os.path.join(out_dir, "vols_no_outliers.txt")
    if os.path.isfile(clean_volumes):
        outputs["clean_volumes"] = clean_volumes

    return outputs
