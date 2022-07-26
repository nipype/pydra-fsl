from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def MELODIC_output(field, inputs):
    import os, attr

    name = field.name
    if name == "out_dir":
        if inputs.out_dir not in [None, attr.NOTHING]:
            outputs = inputs.out_dir
        else:
            outputs = os.getcwd()
    elif name == "report_dir":
        if inputs.report not in [None, attr.NOTHING]:
            if inputs.out_dir not in [None, attr.NOTHING]:
                out_dir = inputs.out_dir
            else:
                out_dir = os.getcwd()
            outputs = os.path.join(out_dir, "report")
    return outputs


input_fields = [
    (
        "in_files",
        specs.MultiInputFile,
        {
            "help_string": "input file names (either single file name or a list)",
            "argstr": "-i {in_files}",
            "mandatory": True,
            "position": 0,
            "sep": ",",
        },
    ),
    (
        "out_dir",
        ty.Any,
        {"help_string": "output directory name", "argstr": "-o {out_dir}"},
    ),
    (
        "mask",
        specs.File,
        {"help_string": "file name of mask for thresholding", "argstr": "-m {mask}"},
    ),
    ("no_mask", bool, {"help_string": "switch off masking", "argstr": "--nomask"}),
    (
        "update_mask",
        bool,
        {"help_string": "switch off mask updating", "argstr": "--update_mask"},
    ),
    ("no_bet", bool, {"help_string": "switch off BET", "argstr": "--nobet"}),
    (
        "bg_threshold",
        float,
        {
            "help_string": "brain/non-brain threshold used to mask non-brain voxels, as a percentage (only if --nobet selected)",
            "argstr": "--bgthreshold={bg_threshold}",
        },
    ),
    (
        "dim",
        int,
        {
            "help_string": "dimensionality reduction into #num dimensions (default: automatic estimation)",
            "argstr": "-d {dim}",
        },
    ),
    (
        "dim_est",
        str,
        {
            "help_string": "use specific dim. estimation technique: lap, bic, mdl, aic, mean (default: lap)",
            "argstr": "--dimest={dim_est}",
        },
    ),
    (
        "sep_whiten",
        bool,
        {"help_string": "switch on separate whitening", "argstr": "--sep_whiten"},
    ),
    (
        "sep_vn",
        bool,
        {
            "help_string": "switch off joined variance normalization",
            "argstr": "--sep_vn",
        },
    ),
    (
        "migp",
        bool,
        {"help_string": "switch on MIGP data reduction", "argstr": "--migp"},
    ),
    (
        "migpN",
        int,
        {"help_string": "number of internal Eigenmaps", "argstr": "--migpN {migpN}"},
    ),
    (
        "migp_shuffle",
        bool,
        {
            "help_string": "randomise MIGP file order (default: TRUE)",
            "argstr": "--migp_shuffle",
        },
    ),
    (
        "migp_factor",
        int,
        {
            "help_string": "Internal Factor of mem-threshold relative to number of Eigenmaps (default: 2)",
            "argstr": "--migp_factor {migp_factor}",
        },
    ),
    (
        "num_ICs",
        int,
        {
            "help_string": "number of IC's to extract (for deflation approach)",
            "argstr": "-n {num_ICs}",
        },
    ),
    (
        "approach",
        str,
        {
            "help_string": "approach for decomposition, 2D: defl, symm (default), 3D: tica (default), concat",
            "argstr": "-a {approach}",
        },
    ),
    (
        "non_linearity",
        str,
        {
            "help_string": "nonlinearity: gauss, tanh, pow3, pow4",
            "argstr": "--nl={non_linearity}",
        },
    ),
    (
        "var_norm",
        bool,
        {"help_string": "switch off variance normalization", "argstr": "--vn"},
    ),
    (
        "pbsc",
        bool,
        {
            "help_string": "switch off conversion to percent BOLD signal change",
            "argstr": "--pbsc",
        },
    ),
    (
        "cov_weight",
        float,
        {
            "help_string": "voxel-wise weights for the covariance matrix (e.g. segmentation information)",
            "argstr": "--covarweight={cov_weight}",
        },
    ),
    (
        "epsilon",
        float,
        {"help_string": "minimum error change", "argstr": "--eps={epsilon}"},
    ),
    (
        "epsilonS",
        float,
        {
            "help_string": "minimum error change for rank-1 approximation in TICA",
            "argstr": "--epsS={epsilonS}",
        },
    ),
    (
        "maxit",
        int,
        {
            "help_string": "maximum number of iterations before restart",
            "argstr": "--maxit={maxit}",
        },
    ),
    (
        "max_restart",
        int,
        {
            "help_string": "maximum number of restarts",
            "argstr": "--maxrestart={max_restart}",
        },
    ),
    (
        "mm_thresh",
        float,
        {
            "help_string": "threshold for Mixture Model based inference",
            "argstr": "--mmthresh={mm_thresh}",
        },
    ),
    (
        "no_mm",
        bool,
        {"help_string": "switch off mixture modelling on IC maps", "argstr": "--no_mm"},
    ),
    (
        "ICs",
        specs.File,
        {
            "help_string": "filename of the IC components file for mixture modelling",
            "argstr": "--ICs={ICs}",
        },
    ),
    (
        "mix",
        specs.File,
        {
            "help_string": "mixing matrix for mixture modelling / filtering",
            "argstr": "--mix={mix}",
        },
    ),
    (
        "smode",
        specs.File,
        {
            "help_string": "matrix of session modes for report generation",
            "argstr": "--smode={smode}",
        },
    ),
    (
        "rem_cmp",
        list,
        {"help_string": "component numbers to remove", "argstr": "-f {rem_cmp}"},
    ),
    (
        "report",
        bool,
        {"help_string": "generate Melodic web report", "argstr": "--report"},
    ),
    (
        "bg_image",
        specs.File,
        {
            "help_string": "specify background image for report (default: mean image)",
            "argstr": "--bgimage={bg_image}",
        },
    ),
    ("tr_sec", float, {"help_string": "TR in seconds", "argstr": "--tr={tr_sec}"}),
    (
        "log_power",
        bool,
        {
            "help_string": "calculate log of power for frequency spectrum",
            "argstr": "--logPower",
        },
    ),
    (
        "t_des",
        specs.File,
        {"help_string": "design matrix across time-domain", "argstr": "--Tdes={t_des}"},
    ),
    (
        "t_con",
        specs.File,
        {
            "help_string": "t-contrast matrix across time-domain",
            "argstr": "--Tcon={t_con}",
        },
    ),
    (
        "s_des",
        specs.File,
        {
            "help_string": "design matrix across subject-domain",
            "argstr": "--Sdes={s_des}",
        },
    ),
    (
        "s_con",
        specs.File,
        {
            "help_string": "t-contrast matrix across subject-domain",
            "argstr": "--Scon={s_con}",
        },
    ),
    ("out_all", bool, {"help_string": "output everything", "argstr": "--Oall"}),
    (
        "out_unmix",
        bool,
        {"help_string": "output unmixing matrix", "argstr": "--Ounmix"},
    ),
    (
        "out_stats",
        bool,
        {
            "help_string": "output thresholded maps and probability maps",
            "argstr": "--Ostats",
        },
    ),
    ("out_pca", bool, {"help_string": "output PCA results", "argstr": "--Opca"}),
    (
        "out_white",
        bool,
        {"help_string": "output whitening/dewhitening matrices", "argstr": "--Owhite"},
    ),
    ("out_orig", bool, {"help_string": "output the original ICs", "argstr": "--Oorig"}),
    ("out_mean", bool, {"help_string": "output mean volume", "argstr": "--Omean"}),
    (
        "report_maps",
        str,
        {
            "help_string": "control string for spatial map images (see slicer)",
            "argstr": "--report_maps={report_maps}",
        },
    ),
    (
        "remove_deriv",
        bool,
        {
            "help_string": "removes every second entry in paradigm file (EV derivatives)",
            "argstr": "--remove_deriv",
        },
    ),
]
MELODIC_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("out_dir", specs.Directory, {"callable": MELODIC_output}),
    ("report_dir", specs.Directory, {"callable": MELODIC_output}),
]
MELODIC_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MELODIC(ShellCommandTask):
    """
    Example
    -------
    >>> task = MELODIC()
    >>> task.inputs.approach = "tica"
    >>> task.inputs.in_files = ['test.nii', 'test2.nii', 'test3.nii']
    >>> task.inputs.no_bet = True
    >>> task.inputs.bg_threshold = 10
    >>> task.inputs.tr_sec = 1.5
    >>> task.inputs.out_stats = True
    >>> task.inputs.t_des = "timeDesign.mat"
    >>> task.inputs.t_con = "timeDesign.con"
    >>> task.inputs.s_des = "subjectDesign.mat"
    >>> task.inputs.s_con = "subjectDesign.con"
    >>> task.inputs.out_dir = "groupICA.out"
    >>> task.cmdline
    'melodic -i test.nii,test2.nii,test3.nii -a tica --bgthreshold=10.000000 --mmthresh=0.500000 --nobet -o groupICA.out --Ostats --Scon=subjectDesign.con --Sdes=subjectDesign.mat --Tcon=timeDesign.con --Tdes=timeDesign.mat --tr=1.500000'
    """

    input_spec = MELODIC_input_spec
    output_spec = MELODIC_output_spec
    executable = "melodic"