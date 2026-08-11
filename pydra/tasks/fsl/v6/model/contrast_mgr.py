import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name in ["param_estimates", "corrections", "dof_file"]:
        return ""
    elif name in ["sigmasquareds"]:
        path, _ = os.path.split(value)
        return path
    else:
        pass

    return argstr.format(**inputs)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    pth, _ = os.path.split(inputs["sigmasquareds"])
    numtcons, numfcons = _get_numcons(
        fcon_file=inputs["fcon_file"],
        tcon_file=inputs["tcon_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    base_contrast = 1
    if inputs["contrast_num"] is not attrs.NOTHING:
        base_contrast = inputs["contrast_num"]
    copes = []
    varcopes = []
    zstats = []
    tstats = []
    neffs = []
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
        neffs.append(
            _gen_fname(
                "neff%d.nii" % (base_contrast + i),
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
        outputs["neffs"] = neffs
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


def copes_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("copes")


def varcopes_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("varcopes")


def zstats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("zstats")


def tstats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("tstats")


def fstats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("fstats")


def zfstats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("zfstats")


def neffs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("neffs")


@shell.define
class ContrastMgr(shell.Task["ContrastMgr.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.model.contrast_mgr import ContrastMgr

    """

    executable = "contrast_mgr"
    tcon_file: File = shell.arg(
        help="contrast file containing T-contrasts", argstr="{tcon_file}", position=-1
    )
    fcon_file: File = shell.arg(
        help="contrast file containing F-contrasts", argstr="-f {fcon_file}"
    )
    param_estimates: list[File] = shell.arg(
        help="Parameter estimates for each column of the design matrix", argstr=""
    )
    corrections: File = shell.arg(
        help="statistical corrections used within FILM modelling"
    )
    dof_file: File = shell.arg(help="degrees of freedom", argstr="")
    sigmasquareds: File = shell.arg(
        help="summary of residuals, See Woolrich, et. al., 2001", argstr="", position=-2
    )
    contrast_num: ty.Any = shell.arg(
        help="contrast number to start labeling copes from", argstr="-cope"
    )
    suffix: str = shell.arg(
        help="suffix to put on the end of the cope filename before the contrast number, default is nothing",
        argstr="-suffix {suffix}",
    )

    class Outputs(shell.Outputs):
        copes: list[File] | None = shell.out(
            help="Contrast estimates for each contrast", callable=copes_callable
        )
        varcopes: list[File] | None = shell.out(
            help="Variance estimates for each contrast", callable=varcopes_callable
        )
        zstats: list[File] | None = shell.out(
            help="z-stat file for each contrast", callable=zstats_callable
        )
        tstats: list[File] | None = shell.out(
            help="t-stat file for each contrast", callable=tstats_callable
        )
        fstats: list[File] | None = shell.out(
            help="f-stat file for each contrast", callable=fstats_callable
        )
        zfstats: list[File] | None = shell.out(
            help="z-stat file for each F contrast", callable=zfstats_callable
        )
        neffs: list[File] | None = shell.out(
            help="neff file ?? for each contrast", callable=neffs_callable
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
        msg = "Unable to generate filename for command %s. " % "contrast_mgr"
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


IFLOGGER = logging.getLogger("nipype.interface")
