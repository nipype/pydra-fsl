from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

def FILMGLS_output(field, inputs):
    import os, attr

    def _get_pe_files(design_file, pth):
        files = None
        if design_file not in [None, attr.NOTHING]:
            fp = open(design_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumWaves"):
                    numpes = int(line.split()[-1])
                    files = []
                    for i in range(numpes):
                        files.append(os.path.join(pth, ("pe%d.nii.gz" % (i + 1))))
                    break
            fp.close()
        return files

    def _get_numcons(inputs):
        numtcons = 0
        numfcons = 0
        if inputs.tcon_file not in [None, attr.NOTHING]:
            fp = open(inputs.tcon_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumContrasts"):
                    numtcons = int(line.split()[-1])
                    break
            fp.close()
        if inputs.fcon_file not in [None, attr.NOTHING]:
            fp = open(inputs.fcon_file, "rt")
            for line in fp.readlines():
                if line.startswith("/NumContrasts"):
                    numfcons = int(line.split()[-1])
                    break
            fp.close()
        return numtcons, numfcons

    name = field.name
    pth = inputs.results_dir       
    if name == "results_dir":
        return pth
    elif name == "param_estimates":
        design_file = inputs.design_file
        pe_files = _get_pe_files(design_file, pth)
        if pe_files:
            return pe_files
    elif name == "residual4d":
        return os.path.join(pth, "res4d.nii.gz")
    elif name == "dof_file":
        return os.path.join(pth, "dof")
    elif name == "sigmasquareds":
        return os.path.join(pth, "sigmasquareds.nii.gz")
    elif name == "thresholdac":
        return os.path.join(pth, "threshac1.nii.gz")
    elif name == "logfile":
        return os.path.join(pth, "logfile")
    
    numtcons, numfcons = _get_numcons(inputs)
    base_contrast = 1
    copes = []
    varcopes = []
    zstats = []
    tstats = []
    for i in range(numtcons):
        copes.append(os.path.join(pth, ("cope%d.nii.gz" % (base_contrast + i))))
        varcopes.append(os.path.join(pth, ("varcope%d.nii.gz" % (base_contrast + i))))
        zstats.append(os.path.join(pth, ("zstat%d.nii.gz" % (base_contrast + i))))
        tstats.append(os.path.join(pth, ("tstat%d.nii.gz" % (base_contrast + i))))
    if copes:
        if name == "copes":
            return copes
        elif name == "varcopes":
            return varcopes
        elif name == "zstats":
            return zstats
        elif name == "tstats":
            return tstats
    fstats = []
    zfstats = []
    for i in range(numfcons):
        fstats.append(os.path.join(pth, ("fstat%d.nii.gz" % (base_contrast + i))))
        zfstats.append(os.path.join(pth, ("zfstat%d.nii.gz" % (base_contrast + i))))
    if fstats:
        if name == "fstats":
            return fstats
        elif name == "zfstats":
            return zfstats



input_fields = [
    
    (
        "in_file",
        specs.File,
        {
            "help_string": "input data file",
            "argstr": "--in={in_file}",
            "mandatory": True,
            "position": -3,
        },
    ),
    (
        "design_file",
        specs.File,
        {
            "help_string": "design matrix file",
            "argstr": "--pd={design_file}",
            "position": -2,
        },
    ),
    (
        "threshold",
        float,
        -1000.0,
        {"help_string": "threshold", "argstr": "--thr={threshold}", "position": -1},
    ),
    (
        "tcon_file",
        specs.File,
        {
            "help_string": "contrast file containing T-contrasts",
            "argstr": "--con={tcon_file}",
        },
    ),
    (
        "fcon_file",
        specs.File,
        {
            "help_string": "contrast file containing F-contrasts",
            "argstr": "--fcon={fcon_file}",
        },
    ),
    (
        "mode",
        ty.Any,
        {"help_string": "Type of analysis to be done", "argstr": "--mode={mode}"},
    ),
    (
        "surface",
        specs.File,
        {
            "help_string": "input surface for autocorr smoothing in surface-based analyses",
            "argstr": "--in2={surface}",
        },
    ),
    (
        "smooth_autocorr",
        bool,
        {"help_string": "Smooth auto corr estimates", "argstr": "--sa"},
    ),
    (
        "mask_size",
        int,
        {"help_string": "susan mask size", "argstr": "--ms={mask_size}"},
    ),
    (
        "brightness_threshold",
        ty.Any,
        {
            "help_string": "susan brightness threshold, otherwise it is estimated",
            "argstr": "--epith={brightness_threshold}",
        },
    ),
    ("full_data", bool, {"help_string": "output full data", "argstr": "-v"}),
    (
        "autocorr_estimate_only",
        bool,
        {
            "help_string": "perform autocorrelation estimation only",
            "argstr": "--ac",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "fit_armodel",
        bool,
        {
            "help_string": "fits autoregressive model - default is to use tukey with M=sqrt(numvols)",
            "argstr": "--ar",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "tukey_window",
        int,
        {
            "help_string": "tukey window size to estimate autocorr",
            "argstr": "--tukey={tukey_window}",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "multitaper_product",
        int,
        {
            "help_string": "multitapering with slepian tapers and num is the time-bandwidth product",
            "argstr": "--mt={multitaper_product}",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "use_pava",
        bool,
        {"help_string": "estimates autocorr using PAVA", "argstr": "--pava"},
    ),
    (
        "autocorr_noestimate",
        bool,
        {
            "help_string": "do not estimate autocorrs",
            "argstr": "--noest",
            "xor": [
                "autocorr_estimate_only",
                "fit_armodel",
                "tukey_window",
                "multitaper_product",
                "use_pava",
                "autocorr_noestimate",
            ],
        },
    ),
    (
        "output_pwdata",
        bool,
        {
            "help_string": "output prewhitened data and average design matrix",
            "argstr": "--outputPWdata",
        },
    ),
    (
        "results_dir",
        str,
        "results",
        {
            "help_string": "directory to store results in",
            "argstr": "--rn={results_dir}"
        },
    ),
]
FILMGLS_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "results_dir",
        specs.Directory,
        {
            "help_string": "Directory storing model estimation output",
            "callable": FILMGLS_output,
        },
    ),
    (
        "param_estimates",
        specs.MultiOutputFile,
        {
            "help_string": "Parameter estimates for each column of the design matrix",
            "callable": FILMGLS_output,
        },
    ),
    (
        "residual4d",
        specs.File,
        {
            "help_string": "Model fit residual mean-squared error for each time point",
            "callable": FILMGLS_output,
        },
    ),
    (
        "dof_file",
        specs.File,
        {"help_string": "degrees of freedom", "callable": FILMGLS_output},
    ),
    (
        "sigmasquareds",
        specs.File,
        {
            "help_string": "summary of residuals, See Woolrich, et. al., 2001",
            "callable": FILMGLS_output,
        },
    ),
    (
        "thresholdac",
        specs.File,
        {
            "help_string": "The FILM autocorrelation parameters",
            "callable": FILMGLS_output,
        },
    ),
    (
        "logfile",
        specs.File,
        {"help_string": "FILM run logfile", "callable": FILMGLS_output},
    ),
    (
        "copes",
        specs.MultiOutputFile,
        {"help_string": "Contrast estimates for each contrast", "requires": ["tcon_file"], "callable": FILMGLS_output},
    ),
    (
        "varcopes",
        specs.MultiOutputFile,
        {"help_string": "Variance estimates for each contrast", "requires": ["tcon_file"], "callable": FILMGLS_output},
    ),
    (
        "zstats",
        specs.MultiOutputFile,
        {"help_string": "z-stat file for each contrast", "requires": ["tcon_file"], "callable": FILMGLS_output},
    ),
    (
        "tstats",
        specs.MultiOutputFile,
        {"help_string": "t-stat file for each contrast","requires": ["tcon_file"], "callable": FILMGLS_output},
    ),
    (
        "fstats",
        specs.MultiOutputFile,
        {"help_string": "f-stat file for each contrast", "requires": ["fcon_file"],"callable": FILMGLS_output},
    ),
    (
        "zfstats",
        specs.MultiOutputFile,
        {"help_string": "z-stat file for each F contrast", "requires": ["fcon_file"], "callable": FILMGLS_output},
    ),
]
FILMGLS_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FILMGLS(ShellCommandTask):
    """
    Example
    -------
    >>> task = FILMGLS()
    >>> task.inputs.in_file = "test.nii"
    >>> task.inputs.design_file = "design.mat"
    >>> task.inputs.threshold = 10
    >>> task.inputs.results_dir = "stats"
    >>> task.cmdline
    'film_gls --in_file=test.nii --pd=design.mat --thr=10'
    """

    input_spec = FILMGLS_input_spec
    output_spec = FILMGLS_output_spec
    executable = "film_gls"