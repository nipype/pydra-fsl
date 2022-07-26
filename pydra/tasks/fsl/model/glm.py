from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file name (text matrix or 3D/4D image file)",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "filename for GLM parameter estimates (GLM betas)",
            "argstr": "-o {out_file}",
            "position": 3,
            "output_file_template": "{in_file}_glm",
        },
    ),
    (
        "design",
        specs.File,
        {
            "help_string": "file name of the GLM design matrix (text time courses for temporal regression or an image file for spatial regression)",
            "argstr": "-d {design}",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "contrasts",
        specs.File,
        {"help_string": "matrix of t-statics contrasts", "argstr": "-c {contrasts}"},
    ),
    (
        "mask",
        specs.File,
        {
            "help_string": "mask image file name if input is image",
            "argstr": "-m {mask}",
        },
    ),
    (
        "dof",
        int,
        {"help_string": "set degrees of freedom explicitly", "argstr": "--dof={dof}"},
    ),
    (
        "des_norm",
        bool,
        {
            "help_string": "switch on normalization of the design matrix columns to unit std deviation",
            "argstr": "--des_norm",
        },
    ),
    (
        "dat_norm",
        bool,
        {
            "help_string": "switch on normalization of the data time series to unit std deviation",
            "argstr": "--dat_norm",
        },
    ),
    (
        "var_norm",
        bool,
        {
            "help_string": "perform MELODIC variance-normalisation on data",
            "argstr": "--vn",
        },
    ),
    (
        "demean",
        bool,
        {
            "help_string": "switch on demeaining of design and data",
            "argstr": "--demean",
        },
    ),
    (
        "out_cope",
        str,
        {
            "help_string": "output file name for COPE (either as txt or image",
            "argstr": "--out_cope={out_cope}",
        },
    ),
    (
        "out_z_name",
        str,
        {
            "help_string": "output file name for Z-stats (either as txt or image",
            "argstr": "--out_z={out_z_name}",
        },
    ),
    (
        "out_t_name",
        str,
        {
            "help_string": "output file name for t-stats (either as txt or image",
            "argstr": "--out_t={out_t_name}",
        },
    ),
    (
        "out_p_name",
        str,
        {
            "help_string": "output file name for p-values of Z-stats (either as text file or image)",
            "argstr": "--out_p={out_p_name}",
        },
    ),
    (
        "out_f_name",
        str,
        {
            "help_string": "output file name for F-value of full model fit",
            "argstr": "--out_f={out_f_name}",
        },
    ),
    (
        "out_pf_name",
        str,
        {
            "help_string": "output file name for p-value for full model fit",
            "argstr": "--out_pf={out_pf_name}",
        },
    ),
    (
        "out_res_name",
        str,
        {
            "help_string": "output file name for residuals",
            "argstr": "--out_res={out_res_name}",
        },
    ),
    (
        "out_varcb_name",
        str,
        {
            "help_string": "output file name for variance of COPEs",
            "argstr": "--out_varcb={out_varcb_name}",
        },
    ),
    (
        "out_sigsq_name",
        str,
        {
            "help_string": "output file name for residual noise variance sigma-square",
            "argstr": "--out_sigsq={out_sigsq_name}",
        },
    ),
    (
        "out_data_name",
        str,
        {
            "help_string": "output file name for pre-processed data",
            "argstr": "--out_data={out_data_name}",
        },
    ),
    (
        "out_vnscales_name",
        str,
        {
            "help_string": "output file name for scaling factors for variance normalisation",
            "argstr": "--out_vnscales={out_vnscales_name}",
        },
    ),
]
GLM_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
GLM_output_spec = specs.SpecInfo(name="Output", fields=output_fields, bases=(specs.ShellOutSpec,))


class GLM(ShellCommandTask):
    """
    Example
    -------
    >>> task = GLM()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.design = "confounds_regressors.tsv"
    >>> task.cmdline # doctest: +ELLIPSIS
    'fsl_glm -i test.nii.gz -d confounds_regressors.tsv'
    """

    input_spec = GLM_input_spec
    output_spec = GLM_output_spec
    executable = "fsl_glm"
