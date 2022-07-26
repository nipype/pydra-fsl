from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def FLAMEO_output(field, inputs):
    import os, glob, attr

    def human_order_sorted(l):
        """
        Sorts string in human order (i.e. 'stat10' will go after 'stat2')
        """

        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            import re

            if isinstance(text, tuple):
                text = text[0]
            return [atoi(c) for c in re.split(r"(\d+)", text)]

        return sorted(l, key=natural_keys)

    pth = inputs.log_dir
    name = field.name

    if name == "pes":
        pes = human_order_sorted(glob.glob(os.path.join(pth, "pe[0-9]*.*")))
        if len(pes) >= 1:
            return pes
    elif name == "res4d":
        res4d = human_order_sorted(glob.glob(os.path.join(pth, "res4d.*")))
        if len(res4d) == 1:
            return res4d[0]
    elif name == "copes":
        copes = human_order_sorted(glob.glob(os.path.join(pth, "cope[0-9]*.*")))
        if len(copes) >= 1:
            return copes
    elif name == "var_copes":
        var_copes = human_order_sorted(glob.glob(os.path.join(pth, "varcope[0-9]*.*")))
        if len(var_copes) >= 1:
            return var_copes
    elif name == "zstats":
        zstats = human_order_sorted(glob.glob(os.path.join(pth, "zstat[0-9]*.*")))
        if len(zstats) >= 1:
            return zstats
    elif name == "tstats":
        tstats = human_order_sorted(glob.glob(os.path.join(pth, "tstat[0-9]*.*")))
        if len(tstats) >= 1:
            return tstats
    elif name == "mrefvars":
        mrefs = human_order_sorted(glob.glob(os.path.join(pth, "mean_random_effects_var[0-9]*.*")))
        if len(mrefs) >= 1:
            return mrefs
    elif name == "tdof":
        tdof = human_order_sorted(glob.glob(os.path.join(pth, "tdof_t[0-9]*.*")))
        if len(tdof) >= 1:
            return tdof
    elif name == "weights":
        weights = human_order_sorted(glob.glob(os.path.join(pth, "weights[0-9]*.*")))
        if len(weights) >= 1:
            return weights
    elif name == "stats_dir":
        return pth
    elif inputs.f_con_file not in [None, attr.NOTHING]:
        if name == "zfstats":
            zfstats = human_order_sorted(glob.glob(os.path.join(pth, "zfstat[0-9]*.*")))
            if len(zfstats) >= 1:
                return zfstats
        elif name == "fstats":
            fstats = human_order_sorted(glob.glob(os.path.join(pth, "fstat[0-9]*.*")))
            if len(fstats) >= 1:
                return fstats
    else:
        raise Exception(
            f"this function should be run only for pes, res4d, copes, var_copes, zfstats,"
            f"fstats, zstats, tstats, mrefs, tdof, weights, or stats_dir, not for {name}"
        )


input_fields = [
    (
        "cope_file",
        specs.File,
        {
            "help_string": "cope regressor data file",
            "argstr": "--copefile={cope_file}",
            "mandatory": True,
        },
    ),
    (
        "var_cope_file",
        specs.File,
        {
            "help_string": "varcope weightings data file",
            "argstr": "--varcopefile={var_cope_file}",
        },
    ),
    (
        "dof_var_cope_file",
        specs.File,
        {
            "help_string": "dof data file for varcope data",
            "argstr": "--dofvarcopefile={dof_var_cope_file}",
        },
    ),
    (
        "mask_file",
        specs.File,
        {
            "help_string": "mask file",
            "argstr": "--maskfile={mask_file}",
            "mandatory": True,
        },
    ),
    (
        "design_file",
        specs.File,
        {
            "help_string": "design matrix file",
            "argstr": "--designfile={design_file}",
            "mandatory": True,
        },
    ),
    (
        "t_con_file",
        specs.File,
        {
            "help_string": "ascii matrix specifying t-contrasts",
            "argstr": "--tcontrastsfile={t_con_file}",
            "mandatory": True,
        },
    ),
    (
        "f_con_file",
        specs.File,
        {
            "help_string": "ascii matrix specifying f-contrasts",
            "argstr": "--fcontrastsfile={f_con_file}",
        },
    ),
    (
        "cov_split_file",
        specs.File,
        {
            "help_string": "ascii matrix specifying the groups the covariance is split into",
            "argstr": "--covsplitfile={cov_split_file}",
            "mandatory": True,
        },
    ),
    (
        "run_mode",
        ty.Any,
        {
            "help_string": "inference to perform",
            "argstr": "--runmode={run_mode}",
            "mandatory": True,
        },
    ),
    (
        "n_jumps",
        int,
        {"help_string": "number of jumps made by mcmc", "argstr": "--njumps={n_jumps}"},
    ),
    (
        "burnin",
        int,
        {
            "help_string": "number of jumps at start of mcmc to be discarded",
            "argstr": "--burnin={burnin}",
        },
    ),
    (
        "sample_every",
        int,
        {
            "help_string": "number of jumps for each sample",
            "argstr": "--sampleevery={sample_every}",
        },
    ),
    ("fix_mean", bool, {"help_string": "fix mean for tfit", "argstr": "--fixmean"}),
    (
        "infer_outliers",
        bool,
        {"help_string": "infer outliers - not for fe", "argstr": "--inferoutliers"},
    ),
    (
        "no_pe_outputs",
        bool,
        {"help_string": "do not output pe files", "argstr": "--nopeoutput"},
    ),
    (
        "sigma_dofs",
        int,
        {
            "help_string": "sigma (in mm) to use for Gaussian smoothing the DOFs in FLAME 2. Default is 1mm, -1 indicates no smoothing",
            "argstr": "--sigma_dofs={sigma_dofs}",
        },
    ),
    (
        "outlier_iter",
        int,
        {
            "help_string": "Number of max iterations to use when inferring outliers. Default is 12.",
            "argstr": "--ioni={outlier_iter}",
        },
    ),
    ("log_dir", ty.Any, "stats", {"help_string": "", "argstr": "--ld={log_dir}"}),
]
FLAMEO_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = [
    (
        "pes",
        specs.MultiOutputFile,
        {
            "help_string": "Parameter estimates for each column of the design matrix for each voxel",
            "callable": FLAMEO_output,
        },
    ),
    (
        "res4d",
        specs.MultiOutputFile,
        {
            "help_string": "Model fit residual mean-squared error for each time point",
            "callable": FLAMEO_output,
        },
    ),
    (
        "copes",
        specs.MultiOutputFile,
        {
            "help_string": "Contrast estimates for each contrast",
            "callable": FLAMEO_output,
        },
    ),
    (
        "var_copes",
        specs.MultiOutputFile,
        {
            "help_string": "Variance estimates for each contrast",
            "callable": FLAMEO_output,
        },
    ),
    (
        "zstats",
        specs.MultiOutputFile,
        {
            "help_string": "z-stat file for each contrast",
            "requires": ["t_con_file"],
            "callable": FLAMEO_output,
        },
    ),
    (
        "tstats",
        specs.MultiOutputFile,
        {
            "help_string": "t-stat file for each contrast",
            "requires": ["t_con_file"],
            "callable": FLAMEO_output,
        },
    ),
    (
        "zfstats",
        specs.MultiOutputFile,
        {
            "help_string": "z stat file for each f contrast",
            "requires": ["f_con_file"],
            "callable": FLAMEO_output,
        },
    ),
    (
        "fstats",
        specs.MultiOutputFile,
        {
            "help_string": "f-stat file for each contrast",
            "requires": ["f_con_file"],
            "callable": FLAMEO_output,
        },
    ),
    (
        "mrefvars",
        specs.MultiOutputFile,
        {
            "help_string": "mean random effect variances for each contrast",
            "callable": FLAMEO_output,
        },
    ),
    (
        "tdof",
        specs.MultiOutputFile,
        {
            "help_string": "temporal dof file for each contrast",
            "callable": FLAMEO_output,
        },
    ),
    (
        "weights",
        specs.MultiOutputFile,
        {"help_string": "weights file for each contrast", "callable": FLAMEO_output},
    ),
    (
        "stats_dir",
        specs.Directory,
        {
            "help_string": "directory storing model estimation output",
            "callable": FLAMEO_output,
        },
    ),
]
FLAMEO_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FLAMEO(ShellCommandTask):
    """
    Example
    -------
    >>> task = FLAMEO()
    >>> task.inputs.cope_file = "cope_merged.nii.gz"
    >>> task.inputs.var_cope_file = "varcope_merged.nii.gz"
    >>> task.inputs.cov_split_file = "design.grp"
    >>> task.inputs.design_file = "design.mat"
    >>> task.inputs.t_con_file = "design.con"
    >>> task.inputs.mask_file = "mask.nii.gz"
    >>> task.inputs.run_mode = "fe"
    >>> task.cmdline
    'flameo --copefile=cope_merged.nii.gz --covsplitfile=design.grp --designfile=design.mat --ld=stats --maskfile=mask.nii.gz --runmode=fe --tcontrastsfile=design.con --varcopefile=varcope_merged.nii.gz'
    """

    input_spec = FLAMEO_input_spec
    output_spec = FLAMEO_output_spec
    executable = "flameo"
