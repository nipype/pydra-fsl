import attrs
from fileformats.generic import Directory, File
import logging
from looseversion import LooseVersion
from pydra.tasks.fsl.v6.base import Info
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    cwd = os.getcwd()
    results_dir = os.path.join(cwd, inputs["results_dir"])
    outputs["results_dir"] = results_dir
    pe_files = _get_pe_files(
        results_dir,
        design_file=inputs["design_file"],
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    if pe_files:
        outputs["param_estimates"] = pe_files
    outputs["residual4d"] = _gen_fname(
        "res4d.nii",
        cwd=results_dir,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["dof_file"] = os.path.join(results_dir, "dof")
    outputs["sigmasquareds"] = _gen_fname(
        "sigmasquareds.nii",
        cwd=results_dir,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["thresholdac"] = _gen_fname(
        "threshac1.nii",
        cwd=results_dir,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    if Info.version() and LooseVersion(Info.version()) < LooseVersion("5.0.7"):
        outputs["corrections"] = _gen_fname(
            "corrections.nii",
            cwd=results_dir,
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    outputs["logfile"] = _gen_fname(
        "logfile",
        change_ext=False,
        cwd=results_dir,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )

    if Info.version() and LooseVersion(Info.version()) > LooseVersion("5.0.6"):
        pth = results_dir
        numtcons, numfcons = _get_numcons(
            fcon_file=inputs["fcon_file"],
            tcon_file=inputs["tcon_file"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
        base_contrast = 1
        copes = []
        varcopes = []
        zstats = []
        tstats = []
        for i in range(numtcons):
            copes.append(
                _gen_fname(
                    "cope%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
            varcopes.append(
                _gen_fname(
                    "varcope%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
            zstats.append(
                _gen_fname(
                    "zstat%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
            tstats.append(
                _gen_fname(
                    "tstat%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
        if copes:
            outputs["copes"] = copes
            outputs["varcopes"] = varcopes
            outputs["zstats"] = zstats
            outputs["tstats"] = tstats
        fstats = []
        zfstats = []
        for i in range(numfcons):
            fstats.append(
                _gen_fname(
                    "fstat%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
            zfstats.append(
                _gen_fname(
                    "zfstat%d.nii" % (base_contrast + i),
                    cwd=pth,
                    output_type=inputs["output_type"],
                    inputs=inputs["inputs"],
                    output_dir=inputs["output_dir"],
                    stderr=inputs["stderr"],
                    stdout=inputs["stdout"],
                )
            )
        if fstats:
            outputs["fstats"] = fstats
            outputs["zfstats"] = zfstats
    return outputs


def param_estimates_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("param_estimates")


def residual4d_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("residual4d")


def dof_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("dof_file")


def sigmasquareds_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("sigmasquareds")


def results_dir_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("results_dir")


def corrections_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("corrections")


def thresholdac_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("thresholdac")


def logfile_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("logfile")


@shell.define(
    xor=[
        [
            "autocorr_estimate_only",
            "autocorr_noestimate",
            "fit_armodel",
            "multitaper_product",
            "tukey_window",
            "use_pava",
        ]
    ]
)
class FILMGLS(shell.Task["FILMGLS.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.fsl.v6.model.filmgls import FILMGLS

    """

    executable = "film_gls"
    in_file: File = shell.arg(help="input data file", argstr="{in_file}", position=-3)
    design_file: File = shell.arg(
        help="design matrix file", argstr="{design_file}", position=-2
    )
    threshold: ty.Any = shell.arg(
        help="threshold", argstr="{threshold}", position=-1, default=1000.0
    )
    smooth_autocorr: bool = shell.arg(help="Smooth auto corr estimates", argstr="-sa")
    mask_size: int = shell.arg(help="susan mask size", argstr="-ms {mask_size}")
    brightness_threshold: ty.Any = shell.arg(
        help="susan brightness threshold, otherwise it is estimated",
        argstr="-epith {brightness_threshold}",
    )
    full_data: bool = shell.arg(help="output full data", argstr="-v")
    autocorr_estimate_only: bool = shell.arg(
        help="perform autocorrelation estimatation only", argstr="-ac"
    )
    fit_armodel: bool = shell.arg(
        help="fits autoregressive model - default is to use tukey with M=sqrt(numvols)",
        argstr="-ar",
    )
    tukey_window: int | None = shell.arg(
        help="tukey window size to estimate autocorr", argstr="-tukey {tukey_window}"
    )
    multitaper_product: int | None = shell.arg(
        help="multitapering with slepian tapers and num is the time-bandwidth product",
        argstr="-mt {multitaper_product}",
    )
    use_pava: bool = shell.arg(help="estimates autocorr using PAVA", argstr="-pava")
    autocorr_noestimate: bool = shell.arg(
        help="do not estimate autocorrs", argstr="-noest"
    )
    output_pwdata: bool = shell.arg(
        help="output prewhitened data and average design matrix",
        argstr="-output_pwdata",
    )
    results_dir: ty.Any = shell.arg(
        help="directory to store results in",
        argstr="-rn {results_dir}",
        default="results",
    )

    class Outputs(shell.Outputs):
        param_estimates: list[File] | None = shell.out(
            help="Parameter estimates for each column of the design matrix",
            callable=param_estimates_callable,
        )
        residual4d: File | None = shell.out(
            help="Model fit residual mean-squared error for each time point",
            callable=residual4d_callable,
        )
        dof_file: File | None = shell.out(
            help="degrees of freedom", callable=dof_file_callable
        )
        sigmasquareds: File | None = shell.out(
            help="summary of residuals, See Woolrich, et. al., 2001",
            callable=sigmasquareds_callable,
        )
        results_dir: Directory | None = shell.out(
            help="directory storing model estimation output",
            callable=results_dir_callable,
        )
        corrections: File | None = shell.out(
            help="statistical corrections used within FILM modeling",
            callable=corrections_callable,
        )
        thresholdac: File | None = shell.out(
            help="The FILM autocorrelation parameters", callable=thresholdac_callable
        )
        logfile: File | None = shell.out(
            help="FILM run logfile", callable=logfile_callable
        )


def _gen_fname(
    basename,
    cwd=None,
    suffix=None,
    change_ext=True,
    ext=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    """Generate a filename based on the given parameters.

    The filename will take the form: cwd/basename<suffix><ext>.
    If change_ext is True, it will use the extensions specified in
    <instance>inputs.output_type.

    Parameters
    ----------
    basename : str
        Filename to base the new filename on.
    cwd : str
        Path to prefix to the new filename. (default is output_dir)
    suffix : str
        Suffix to add to the `basename`.  (defaults is '' )
    change_ext : bool
        Flag to change the filename extension to the FSL output type.
        (default True)

    Returns
    -------
    fname : str
        New filename based on given parameters.

    """

    if basename == "":
        msg = "Unable to generate filename for command %s. " % "film_gls"
        msg += "basename is not set!"
        raise ValueError(msg)
    if cwd is None:
        cwd = output_dir
    if ext is None:
        ext = Info.output_type_to_ext(output_type)
    if change_ext:
        if suffix:
            suffix = f"{suffix}{ext}"
        else:
            suffix = ext
    if suffix is None:
        suffix = ""
    fname = fname_presuffix(basename, suffix=suffix, use_ext=False, newpath=cwd)
    return fname


def _get_numcons(
    fcon_file=None,
    tcon_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    numtcons = 0
    numfcons = 0
    if tcon_file is not attrs.NOTHING:
        with open(tcon_file) as fp:
            for line in fp:
                if line.startswith("/NumContrasts"):
                    numtcons = int(line.split()[-1])
                    break
    if fcon_file is not attrs.NOTHING:
        with open(fcon_file) as fp:
            for line in fp:
                if line.startswith("/NumContrasts"):
                    numfcons = int(line.split()[-1])
                    break
    return numtcons, numfcons


def _get_pe_files(
    cwd,
    design_file=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    files = None
    if design_file is not attrs.NOTHING:
        with open(design_file) as fp:
            for line in fp:
                if line.startswith("/NumWaves"):
                    numpes = int(line.split()[-1])
                    files = [
                        _gen_fname(f"pe{i + 1}.nii", cwd=cwd, output_type=output_type)
                        for i in range(numpes)
                    ]
                    break
    return files


IFLOGGER = logging.getLogger("nipype.interface")
