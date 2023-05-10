from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "File containing all the images to estimate distortions for",
            "argstr": "--imain={in_file}",
            "mandatory": True,
        },
    ),
    (
        "in_mask",
        specs.File,
        {
            "help_string": "Mask to indicate brain",
            "argstr": "--mask={in_mask}",
            "mandatory": True,
        },
    ),
    (
        "in_index",
        specs.File,
        {
            "help_string": "File containing indices for all volumes in --imain into --acqp and --topup",
            "argstr": "--index={in_index}",
            "mandatory": True,
        },
    ),
    (
        "in_acqp",
        specs.File,
        {
            "help_string": "File containing acquisition parameters",
            "argstr": "--acqp={in_acqp}",
            "mandatory": True,
        },
    ),
    (
        "in_bvec",
        specs.File,
        {
            "help_string": "File containing the b-vectors for all volumes in --imain",
            "argstr": "--bvecs={in_bvec}",
            "mandatory": True,
        },
    ),
    (
        "in_bval",
        specs.File,
        {
            "help_string": "File containing the b-values for all volumes in --imain",
            "argstr": "--bvals={in_bval}",
            "mandatory": True,
        },
    ),
    (
        "out_base",
        str,
        "eddy_corrected",
        {"help_string": "Basename for output image", "argstr": "--out={out_base}"},
    ),
    (
        "session",
        specs.File,
        {
            "help_string": "File containing session indices for all volumes in --imain",
            "argstr": "--session={session}",
        },
    ),
    (
        "in_topup_fieldcoef",
        specs.File,
        {
            "help_string": "Topup results file containing the field coefficients",
            "argstr": "--topup={in_topup_fieldcoef}",
            "requires": ["in_topup_movpar"],
        },
    ),
    (
        "in_topup_movpar",
        specs.File,
        {
            "help_string": "Topup results file containing the movement parameters (movpar.txt)",
            "requires": ["in_topup_fieldcoef"],
        },
    ),
    (
        "field",
        specs.File,
        {
            "help_string": "Non-topup derived fieldmap scaled in Hz",
            "argstr": "--field={field}",
        },
    ),
    (
        "field_mat",
        specs.File,
        {
            "help_string": "Matrix specifying the relative positions of the fieldmap, --field, and the first volume of the input file, --imain",
            "argstr": "--field_mat={field_mat}",
        },
    ),
    (
        "flm",
        ty.Any,
        "quadratic",
        {"help_string": "First level EC model", "argstr": "--flm={flm}"},
    ),
    (
        "slm",
        ty.Any,
        "none",
        {"help_string": "Second level EC model", "argstr": "--slm={slm}"},
    ),
    (
        "fep",
        bool,
        {"help_string": "Fill empty planes in x- or y-directions", "argstr": "--fep"},
    ),
    (
        "initrand",
        bool,
        {
            "help_string": "Resets rand for when selecting voxels",
            "argstr": "--initrand",
        },
    ),
    (
        "interp",
        ty.Any,
        "spline",
        {
            "help_string": "Interpolation model for estimation step",
            "argstr": "--interp={interp}",
        },
    ),
    (
        "nvoxhp",
        int,
        1000,
        {
            "help_string": "# of voxels used to estimate the hyperparameters",
            "argstr": "--nvoxhp={nvoxhp}",
        },
    ),
    (
        "fudge_factor",
        float,
        10.0,
        {
            "help_string": "Fudge factor for hyperparameter error variance",
            "argstr": "--ff={fudge_factor}",
        },
    ),
    (
        "dont_sep_offs_move",
        bool,
        {
            "help_string": "Do NOT attempt to separate field offset from subject movement",
            "argstr": "--dont_sep_offs_move",
        },
    ),
    (
        "dont_peas",
        bool,
        {
            "help_string": "Do NOT perform a post-eddy alignment of shells",
            "argstr": "--dont_peas",
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "FWHM for conditioning filter when estimating the parameters",
            "argstr": "--fwhm={fwhm}",
        },
    ),
    (
        "niter",
        int,
        5,
        {"help_string": "Number of iterations", "argstr": "--niter={niter}"},
    ),
    (
        "method",
        ty.Any,
        "jac",
        {
            "help_string": "Final resampling method (jacobian/least squares)",
            "argstr": "--resamp={method}",
        },
    ),
    (
        "repol",
        bool,
        {"help_string": "Detect and replace outlier slices", "argstr": "--repol"},
    ),
    (
        "outlier_nstd",
        int,
        {
            "help_string": "Number of std off to qualify as outlier",
            "argstr": "--ol_nstd",
            "requires": ["repol"],
        },
    ),
    (
        "outlier_nvox",
        int,
        {
            "help_string": "Min # of voxels in a slice for inclusion in outlier detection",
            "argstr": "--ol_nvox",
            "requires": ["repol"],
        },
    ),
    (
        "outlier_type",
        ty.Any,
        {
            "help_string": "Type of outliers, slicewise (sw), groupwise (gw) or both (both)",
            "argstr": "--ol_type",
            "requires": ["repol"],
        },
    ),
    (
        "outlier_pos",
        bool,
        {
            "help_string": "Consider both positive and negative outliers if set",
            "argstr": "--ol_pos",
            "requires": ["repol"],
        },
    ),
    (
        "outlier_sqr",
        bool,
        {
            "help_string": "Consider outliers among sums-of-squared differences if set",
            "argstr": "--ol_sqr",
            "requires": ["repol"],
        },
    ),
    (
        "multiband_factor",
        int,
        {"help_string": "Multi-band factor", "argstr": "--mb={multiband_factor}"},
    ),
    (
        "multiband_offset",
        ty.Any,
        {
            "help_string": "Multi-band offset (-1 if bottom slice removed, 1 if top slice removed",
            "argstr": "--mb_offs={multiband_offset}",
            "requires": ["multiband_factor"],
        },
    ),
    (
        "mporder",
        int,
        {
            "help_string": "Order of slice-to-vol movement model",
            "argstr": "--mporder={mporder}",
            "requires": ["use_cuda"],
        },
    ),
    (
        "slice2vol_niter",
        int,
        {
            "help_string": "Number of iterations for slice-to-vol",
            "argstr": "--s2v_niter={slice2vol_niter}",
            "requires": ["mporder"],
        },
    ),
    (
        "slice2vol_lambda",
        int,
        {
            "help_string": "Regularisation weight for slice-to-vol movement (reasonable range 1-10)",
            "argstr": "--s2v_lambda={slice2vol_lambda}",
            "requires": ["mporder"],
        },
    ),
    (
        "slice2vol_interp",
        ty.Any,
        {
            "help_string": "Slice-to-vol interpolation model for estimation step",
            "argstr": "--s2v_interp={slice2vol_interp}",
            "requires": ["mporder"],
        },
    ),
    (
        "slice_order",
        ty.Any,
        {
            "help_string": "Name of text file completely specifying slice/group acquisition",
            "argstr": "--slspec={slice_order}",
            "requires": ["mporder"],
            "xor": ["json"],
        },
    ),
    (
        "json",
        ty.Any,
        {
            "help_string": "Name of .json text file with information about slice timing",
            "argstr": "--json={json}",
            "requires": ["mporder"],
            "xor": ["slice_order"],
        },
    ),
    (
        "estimate_move_by_susceptibility",
        bool,
        {
            "help_string": "Estimate how susceptibility field changes with subject movement",
            "argstr": "--estimate_move_by_susceptibility",
        },
    ),
    (
        "mbs_niter",
        int,
        {
            "help_string": "Number of iterations for MBS estimation",
            "argstr": "--mbs_niter={mbs_niter}",
            "requires": ["estimate_move_by_susceptibility"],
        },
    ),
    (
        "mbs_lambda",
        int,
        {
            "help_string": "Weighting of regularisation for MBS estimation",
            "argstr": "--mbs_lambda={mbs_lambda}",
            "requires": ["estimate_move_by_susceptibility"],
        },
    ),
    (
        "mbs_ksp",
        int,
        {
            "help_string": "Knot-spacing for MBS field estimation",
            "argstr": "--mbs_ksp={mbs_ksp}mm",
            "requires": ["estimate_move_by_susceptibility"],
        },
    ),
    ("num_threads", int, 1, {"help_string": "Number of openmp threads to use"}),
    (
        "is_shelled",
        bool,
        {
            "help_string": "Override internal check to ensure that date are acquired on a set of b-value shells",
            "argstr": "--data_is_shelled",
        },
    ),
    ("use_cuda", bool, {"help_string": "Run eddy using cuda gpu"}),
    ("cnr_maps", bool, {"help_string": "Output CNR-Maps", "argstr": "--cnr_maps"}),
    ("residuals", bool, {"help_string": "Output Residuals", "argstr": "--residuals"}),
]
Eddy_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "out_corrected",
        specs.File,
        {
            "help_string": "4D image file containing all the corrected volumes",
            "output_file_template": "{out_base}.nii.gz",
        },
    ),
    (
        "out_parameter",
        specs.File,
        {
            "help_string": "Text file with parameters defining the field and movement for each scan",
            "output_file_template": "{out_base}.eddy_parameters",
        },
    ),
    (
        "out_movement_rms",
        specs.File,
        {
            "help_string": "Summary of the 'total movement' in each volume",
            "output_file_template": "{out_base}.eddy_movement_rms",
        },
    ),
    (
        "out_restricted_movement_rms",
        specs.File,
        {
            "help_string": "Summary of the 'total movement' in each volume disregarding translation in the PE direction",
            "output_file_template": "{out_base}.eddy_restricted_movement_rms",
        },
    ),
    (
        "out_shell_alignment_parameters",
        specs.File,
        {
            "help_string": "Text file containing rigid body movement parameters between the different shells as estimated by a post-hoc mutual information based registration",
            "output_file_template": "{out_base}.eddy_post_eddy_shell_alignment_parameters",
        },
    ),
    (
        "out_shell_pe_translation_parameters",
        specs.File,
        {
            "help_string": "Text file containing translation along the PE-direction between the different shells as estimated by a post-hoc mutual information based registration",
            "output_file_template": "{out_base}.eddy_post_eddy_shell_PE_translation_parameters",
        },
    ),
    (
        "out_outlier_map",
        specs.File,
        {
            "help_string": 'Matrix where rows represent volumes and columns represent slices. "0" indicates that scan-slice is not an outlier and "1" indicates that it is',
            "output_file_template": "{out_base}.eddy_outlier_map",
        },
    ),
    (
        "out_outlier_n_stdev_map",
        specs.File,
        {
            "help_string": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deviations off the mean difference between observation and prediction is",
            "output_file_template": "{out_base}.eddy_outlier_n_stdev_map",
        },
    ),
    (
        "out_outlier_n_sqr_stdev_map",
        specs.File,
        {
            "help_string": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deivations off the square root of the mean squared difference between observation and prediction is",
            "output_file_template": "{out_base}.eddy_outlier_n_sqr_stdev_map",
        },
    ),
    (
        "out_outlier_report",
        specs.File,
        {
            "help_string": "Text file with a plain language report on what outlier slices eddy has found",
            "output_file_template": "{out_base}.eddy_outlier_report",
        },
    ),
    (
        "out_outlier_free",
        specs.File,
        {
            "help_string": "4D image file not corrected for susceptibility or eddy-current distortions or subject movement but with outlier slices replaced",
            "requires": ["repol"],
            "output_file_template": "{out_base}.eddy_outlier_free_data",
        },
    ),
    (
        "out_movement_over_time",
        specs.File,
        {
            "help_string": "Text file containing translations (mm) and rotations (radians) for each excitation",
            "requires": ["mporder"],
            "output_file_template": "{out_base}.eddy_movement_over_time",
        },
    ),
    (
        "out_cnr_maps",
        specs.File,
        {
            "help_string": "path/name of file with the cnr_maps",
            "requires": ["cnr_maps"],
            "output_file_template": "{out_base}.eddy_cnr_maps",
        },
    ),
    (
        "out_residuals",
        specs.File,
        {
            "help_string": "path/name of file with the residuals",
            "requires": ["residuals"],
            "output_file_template": "{out_base}.eddy_residuals",
        },
    ),
]
Eddy_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Eddy(ShellCommandTask):
    """
    Example
    -------
    >>> task = Eddy()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.in_mask = "mask.nii.gz"
    >>> task.inputs.in_index = "test_index.txt"
    >>> task.inputs.in_acqp = "test_acqp.txt"
    >>> task.inputs.in_bvec = "bvecs.scheme"
    >>> task.inputs.in_bval = "bvals.scheme"
    >>> task.cmdline
    'eddy_openmp --imain=test.nii.gz --mask=test_mask.nii.gz --index=test_index.txt --acqp=test_acqp.txt --bvecs=bvecs.scheme --bvals=bvals.scheme --verbose'
    """

    input_spec = Eddy_input_spec
    output_spec = Eddy_output_spec
    executable = "eddy_openmp"
