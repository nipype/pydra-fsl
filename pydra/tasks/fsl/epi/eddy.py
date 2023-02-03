from pydra.engine import specs
from pydra import ShellCommandTask

input_fields = [
    (
        "in_acqp",
        str,
        {
            "help_string": "File containing acquisition parameters.",
            "argstr": "--acqp={in_acqp}",
            "mandatory": True,
        },
    ),
    (
        "in_bval",
        str,
        {
            "help_string": "File containing the b-values for all volumes in –imain.",
            "argstr": "--bvals={in_bval}",
            "mandatory": True,
        },
    ),
    (
        "in_bvec",
        str,
        {
            "help_string": "File containing the b-vectors for all volumes in –imain.",
            "argstr": "--bvecs={in_bvec}",
            "mandatory": True,
        },
    ),
    (
        "in_file",
        str,
        {
            "help_string": "File containing all the images to estimate distortions for.",
            "argstr": "--imain={in_file}",
            "mandatory": True,
        },
    ),
    (
        "in_index",
        str,
        {
            "help_string": "File containing indices for all volumes in –imain into –acqp and –topup.",
            "argstr": "--index={in_index}",
            "mandatory": True,
        },
    ),
    (
        "in_mask",
        str,
        {
            "help_string": "Mask to indicate brain.",
            "argstr": "--mask={in_mask}",
            "mandatory": True,
        },
    ),
    (
        "cnr_maps",
        bool,
        {
            "help_string": "Output CNR-Maps.",
            "argstr": "--cnr_maps",
        },
    ),
    (
        "dont_peas",
        bool,
        {
            "help_string": "Do NOT perform a post-eddy alignment of shells.",
            "argstr": "--dont_peas",
        },
    ),
    (
        "dont_sep_offs_move",
        bool,
        {
            "help_string": "Do NOT attempt to separate field offset from subject movement.",
            "argstr": "--dont_sep_offs_move",
        },
    ),
    (
        "estimate_move_by_susceptibility",
        bool,
        {
            "help_string": "Estimate how susceptibility field changes with subject movement.",
            "argstr": "--estimate_move_by_susceptibility",
        },
    ),
    (
        "fep",
        bool,
        {
            "help_string": "Fill empty planes in x- or y-directions.",
            "argstr": "--fep",
        },
    ),
    (
        "field",
        specs.File,
        {
            "help_string": "Non-topup derived fieldmap scaled in Hz.",
            "argstr": "--field={field}",
        },
    ),
    (
        "field_mat",
        specs.File,
        {
            "help_string": (
                "Matrix specifying the relative positions of the fieldmap, –field, "
                "and the first volume of the input file, –imain."
            ),
            "argstr": "--field_mat={field_mat}",
        },
    ),
    (
        "flm",  # (‘quadratic’ or ‘linear’ or ‘cubic’)
        str,
        {
            "help_string": "First level EC model.",
            "argstr": "--flm={flm}",
        },
    ),
    (
        "fudge_factor",
        float,
        {
            "help_string": "Fudge factor for hyperparameter error variance.",
            "argstr": "--ff={fudge_factor}",
        },
    ),
    (
        "fwhm",
        float,
        {
            "help_string": "FWHM for conditioning filter when estimating the parameters.",
            "argstr": "--fwhm={fwhm}",
        },
    ),
    (
        "in_topup_fieldcoef",
        specs.File,
        {
            "help_string": "Topup results file containing the field coefficients.",
            "argstr": "--topup={in_topup_fieldcoef}",
            "requires": [
                "in_topup_movpar",
            ],
        },
    ),
    (
        "in_topup_movpar",
        specs.File,
        {
            "help_string": "Topup results file containing the movement parameters (movpar.txt).",
            "requires": [
                "in_topup_fieldcoef",
            ],
        },
    ),
    (
        "initrand",
        bool,
        {
            "help_string": "Resets rand for when selecting voxels.",
            "argstr": "--initrand",
        },
    ),
    (
        "interp",  # (‘spline’ or ‘trilinear’)
        str,
        {
            "help_string": "Interpolation model for estimation step.",
            "argstr": "--interp=%s",
        },
    ),
    (
        "is_shelled",
        bool,
        {
            "help_string": (
                "Override internal check to ensure that date are "
                "acquired on a set of b-value shells."
            ),
            "argstr": "--data_is_shelled",
        },
    ),
    (
        "json",
        specs.File,
        {
            "help_string": "Name of .json text file with information about slice timing.",
            "argstr": "--json={json}",
            "xor": ("slice_order",),
            "requires": [
                "mporder",
            ],
        },
    ),
    (
        "mbs_ksp",
        int,
        {
            "help_string": "Knot-spacing for MBS field estimation.",
            "argstr": "--mbs_ksp={mbs_ksp}mm",
            "requires": [
                "estimate_move_by_susceptibility",
            ],
        },
    ),
    (
        "mbs_lambda",
        int,
        {
            "help_string": "Weighting of regularisation for MBS estimation.",
            "argstr": "--mbs_lambda={mbs_lambda}",
            "requires": [
                "estimate_move_by_susceptibility",
            ],
        },
    ),
    (
        "mbs_niter",
        int,
        {
            "help_string": "Number of iterations for MBS estimation.",
            "argstr": "--mbs_niter={mbs_niter}",
            "requires": [
                "estimate_move_by_susceptibility",
            ],
        },
    ),
    (
        "method",  # (‘jac’ or ‘lsr’)
        str,
        {
            "help_string": "Final resampling method (jacobian/least squares).",
            "argstr": "--resamp={method}",
        },
    ),
    (
        "mporder",
        int,
        {
            "help_string": "Order of slice-to-vol movement model.",
            "argstr": "--mporder={mporder}",
            "requires": [
                "use_cuda",
            ],
        },
    ),
    (
        "multiband_factor",
        int,
        {
            "help_string": "Multi-band factor.",
            "argstr": "--mb={multiband_factor}",
        },
    ),
    (
        "multiband_offset",  # (0 or 1 or -1)
        int,
        {
            "help_string": "Multi-band offset (-1 if bottom slice removed, 1 if top slice removed.",
            "argstr": "--mb_offs={multiband_offset}",
            "requires": [
                "multiband_factor",
            ],
        },
    ),
    (
        "niter",
        int,
        {
            "help_string": "Number of iterations.",
            "argstr": "--niter={niter}",
        },
    ),
    (
        "num_threads",
        int,
        {
            "help_string": "Number of openmp threads to use.",
        },
    ),
    (
        "nvoxhp",
        int,
        {
            "help_string": "Number of voxels used to estimate the hyperparameters.",
            "argstr": "--nvoxhp={nvoxhp}",
        },
    ),
    (
        "out_base",
        str,
        {
            "help_string": "Basename for output image.",
            "argstr": "--out={out_base}",
        },
    ),
    (
        "outlier_nstd",
        int,
        {
            "help_string": "Number of std off to qualify as outlier.",
            "argstr": "--ol_nstd",
            "requires": [
                "repol",
            ],
        },
    ),
    (
        "outlier_nvox",
        int,
        {
            "help_string": "Min number of voxels in a slice for inclusion in outlier detection.",
            "argstr": "--ol_nvox",
            "requires": [
                "repol",
            ],
        },
    ),
    (
        "outlier_pos",
        bool,
        {
            "help_string": "Consider both positive and negative outliers if set.",
            "argstr": "--ol_pos",
            "requires": [
                "repol",
            ],
        },
    ),
    (
        "outlier_sqr",
        bool,
        {
            "help_string": "Consider outliers among sums-of-squared differences if set.",
            "argstr": "--ol_sqr",
            "requires": [
                "repol",
            ],
        },
    ),
    (
        "outlier_type",  # (‘sw’ or ‘gw’ or ‘both’)
        str,
        {
            "help_string": "Type of outliers, slicewise (sw), groupwise (gw) or both (both).",
            "argstr": "--ol_type",
            "requires": [
                "repol",
            ],
        },
    ),
    (
        "output_type",  # (‘NIFTI’ or ‘NIFTI_PAIR’ or ‘NIFTI_GZ’ or ‘NIFTI_PAIR_GZ’)
        str,
        {
            "help_string": "FSL output type.",
        },
    ),
    (
        "repol",
        bool,
        {
            "help_string": "Detect and replace outlier slices.",
            "argstr": "--repol",
        },
    ),
    (
        "residuals",
        bool,
        {
            "help_string": "Output Residuals.",
            "argstr": "--residuals",
        },
    ),
    (
        "session",
        specs.File,
        {
            "help_string": "File containing session indices for all volumes in –imain.",
            "argstr": "--session={session}",
        },
    ),
    (
        "slice2vol_interp",  # (‘trilinear’ or ‘spline’)
        str,
        {
            "help_string": "Slice-to-vol interpolation model for estimation step.",
            "argstr": "--s2v_interp={slice2vol_interp",
            "requires": [
                "mporder",
            ],
        },
    ),
    (
        "slice2vol_lambda",
        int,
        {
            "help_string": "Regularisation weight for slice-to-vol movement (reasonable range 1-10).",
            "argstr": "--s2v_lambda={slice2vol_lambda}",
            "requires": [
                "mporder",
            ],
        },
    ),
    (
        "slice2vol_niter",
        int,
        {
            "help_string": "Number of iterations for slice-to-vol.",
            "argstr": "--s2v_niter={slice2vol_niter}",
            "requires": [
                "mporder",
            ],
        },
    ),
    (
        "slice_order",
        specs.File,
        {
            "help_string": "Name of text file completely specifying slice/group acquisition.",
            "argstr": "--slspec={slice_order}",
            "xor": ("json",),
            "requires": [
                "mporder",
            ],
        },
    ),
    (
        "slm",  # (‘none’ or ‘linear’ or ‘quadratic’)
        str,
        {
            "help_string": "Second level EC model.",
            "argstr": "--slm={slm}",
        },
    ),
    (
        "use_cuda",
        bool,
        {
            "help_string": "Run eddy using cuda gpu.",
        },
    ),
]

eddy_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []

eddy_output_spec = specs.SpecInfo(name="Output", fields=output_fields, bases=(specs.ShellOutSpec,))


class Eddy(ShellCommandTask):
    """
        Example
        -------
    >>> eddy = Eddy()
    >>> eddy.inputs.in_file = "epi.nii"
    >>> eddy.inputs.in_mask = "epi_mask.nii"
    >>> eddy.inputs.in_index = "epi_index.txt"
    >>> eddy.inputs.in_acqp = "epi_acqp.txt"
    >>> eddy.inputs.in_bvec = "bvecs.scheme"
    >>> eddy.inputs.in_bval = "bvals.scheme"
    >>> eddy.cmdline
        ‘eddy_openmp –flm=quadratic –ff=10.0 –acqp=epi_acqp.txt –bvals=bvals.scheme –bvecs=bvecs.scheme –imain=epi.nii –index=epi_index.txt –mask=epi_mask.nii –interp=spline –resamp=jac –niter=5 –nvoxhp=1000 –out=…/eddy_corrected –slm=none’
    """

    input_spec = eddy_input_spec
    output_spec = eddy_output_spec
    executable = "eddy_openmp"
