"""Module to put any functions that are referred to in the "callables" section of Eddy.yaml"""

import attrs
import os


def out_cnr_maps_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_cnr_maps"]


def out_corrected_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_corrected"]


def out_movement_over_time_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_movement_over_time"]


def out_movement_rms_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_movement_rms"]


def out_outlier_free_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_outlier_free"]


def out_outlier_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_outlier_map"]


def out_outlier_n_sqr_stdev_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_outlier_n_sqr_stdev_map"]


def out_outlier_n_stdev_map_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_outlier_n_stdev_map"]


def out_outlier_report_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_outlier_report"]


def out_parameter_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_parameter"]


def out_residuals_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_residuals"]


def out_restricted_movement_rms_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_restricted_movement_rms"]


def out_rotated_bvecs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_rotated_bvecs"]


def out_shell_alignment_parameters_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_shell_alignment_parameters"]


def out_shell_pe_translation_parameters_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs["out_shell_pe_translation_parameters"]


# Original source at L885 of <nipype-install>/interfaces/base/core.py
def _gen_filename(name, inputs=None, stdout=None, stderr=None, output_dir=None):
    raise NotImplementedError


# Original source at L1008 of <nipype-install>/interfaces/fsl/epi.py
def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    outputs = {}
    outputs["out_corrected"] = os.path.abspath("%s.nii.gz" % inputs.out_base)
    outputs["out_parameter"] = os.path.abspath("%s.eddy_parameters" % inputs.out_base)

    # File generation might depend on the version of EDDY
    out_rotated_bvecs = os.path.abspath("%s.eddy_rotated_bvecs" % inputs.out_base)
    out_movement_rms = os.path.abspath("%s.eddy_movement_rms" % inputs.out_base)
    out_restricted_movement_rms = os.path.abspath(
        "%s.eddy_restricted_movement_rms" % inputs.out_base
    )
    out_shell_alignment_parameters = os.path.abspath(
        "%s.eddy_post_eddy_shell_alignment_parameters" % inputs.out_base
    )
    out_shell_pe_translation_parameters = os.path.abspath(
        "%s.eddy_post_eddy_shell_PE_translation_parameters" % inputs.out_base
    )
    out_outlier_map = os.path.abspath("%s.eddy_outlier_map" % inputs.out_base)
    out_outlier_n_stdev_map = os.path.abspath(
        "%s.eddy_outlier_n_stdev_map" % inputs.out_base
    )
    out_outlier_n_sqr_stdev_map = os.path.abspath(
        "%s.eddy_outlier_n_sqr_stdev_map" % inputs.out_base
    )
    out_outlier_report = os.path.abspath("%s.eddy_outlier_report" % inputs.out_base)
    if (inputs.repol is not attrs.NOTHING) and inputs.repol:
        out_outlier_free = os.path.abspath(
            "%s.eddy_outlier_free_data" % inputs.out_base
        )
        if os.path.exists(out_outlier_free):
            outputs["out_outlier_free"] = out_outlier_free
    if (inputs.mporder is not attrs.NOTHING) and inputs.mporder > 0:
        out_movement_over_time = os.path.abspath(
            "%s.eddy_movement_over_time" % inputs.out_base
        )
        if os.path.exists(out_movement_over_time):
            outputs["out_movement_over_time"] = out_movement_over_time
    if (inputs.cnr_maps is not attrs.NOTHING) and inputs.cnr_maps:
        out_cnr_maps = os.path.abspath("%s.eddy_cnr_maps.nii.gz" % inputs.out_base)
        if os.path.exists(out_cnr_maps):
            outputs["out_cnr_maps"] = out_cnr_maps
    if (inputs.residuals is not attrs.NOTHING) and inputs.residuals:
        out_residuals = os.path.abspath("%s.eddy_residuals.nii.gz" % inputs.out_base)
        if os.path.exists(out_residuals):
            outputs["out_residuals"] = out_residuals

    if os.path.exists(out_rotated_bvecs):
        outputs["out_rotated_bvecs"] = out_rotated_bvecs
    if os.path.exists(out_movement_rms):
        outputs["out_movement_rms"] = out_movement_rms
    if os.path.exists(out_restricted_movement_rms):
        outputs["out_restricted_movement_rms"] = out_restricted_movement_rms
    if os.path.exists(out_shell_alignment_parameters):
        outputs["out_shell_alignment_parameters"] = out_shell_alignment_parameters
    if os.path.exists(out_shell_pe_translation_parameters):
        outputs["out_shell_pe_translation_parameters"] = (
            out_shell_pe_translation_parameters
        )
    if os.path.exists(out_outlier_map):
        outputs["out_outlier_map"] = out_outlier_map
    if os.path.exists(out_outlier_n_stdev_map):
        outputs["out_outlier_n_stdev_map"] = out_outlier_n_stdev_map
    if os.path.exists(out_outlier_n_sqr_stdev_map):
        outputs["out_outlier_n_sqr_stdev_map"] = out_outlier_n_sqr_stdev_map
    if os.path.exists(out_outlier_report):
        outputs["out_outlier_report"] = out_outlier_report

    return outputs
