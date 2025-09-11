import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import nibabel as nb
from pydra.tasks.fsl.v6.base import Info
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import (
    fname_presuffix,
    split_filename,
)
import numpy as np
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
from pydra.utils.typing import MultiInputObj
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "encoding_direction":
        return argstr.format(
            **{
                name: _generate_encfile(
                    encoding_direction=inputs["encoding_direction"],
                    in_file=inputs["in_file"],
                    readout_times=inputs["readout_times"],
                )
            }
        )
    if name == "out_base":
        path, name, ext = split_filename(value)
        if path != "":
            if not os.path.exists(path):
                raise ValueError("out_base path must exist if provided")

    return argstr.format(**inputs)


def encoding_direction_formatter(field, inputs):
    return _format_arg(
        "encoding_direction", field, inputs, argstr="--datain={encoding_direction}"
    )


def out_base_formatter(field, inputs):
    return _format_arg("out_base", field, inputs, argstr="--out={out_base}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    del outputs["out_base"]
    base_path = None
    if inputs["out_base"] is not attrs.NOTHING:
        base_path, base, _ = split_filename(inputs["out_base"])
        if base_path == "":
            base_path = None
    else:
        base = split_filename(inputs["in_file"])[1] + "_base"
    outputs["out_fieldcoef"] = _gen_fname(
        base,
        suffix="_fieldcoef",
        cwd=base_path,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["out_movpar"] = _gen_fname(
        base,
        suffix="_movpar",
        ext=".txt",
        cwd=base_path,
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )

    n_vols = nb.load(inputs["in_file"]).shape[-1]
    ext = Info.output_type_to_ext(inputs["output_type"])
    fmt = os.path.abspath("{prefix}_{i:02d}{ext}").format
    outputs["out_warps"] = [
        fmt(prefix=inputs["out_warp_prefix"], i=i, ext=ext)
        for i in range(1, n_vols + 1)
    ]
    outputs["out_jacs"] = [
        fmt(prefix=inputs["out_jac_prefix"], i=i, ext=ext) for i in range(1, n_vols + 1)
    ]
    outputs["out_mats"] = [
        fmt(prefix=inputs["out_mat_prefix"], i=i, ext=".mat")
        for i in range(1, n_vols + 1)
    ]

    if inputs["encoding_direction"] is not attrs.NOTHING:
        outputs["out_enc_file"] = _get_encfilename(
            in_file=inputs["in_file"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    return outputs


def out_fieldcoef_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_fieldcoef")


def out_movpar_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_movpar")


def out_enc_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_enc_file")


def out_warps_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_warps")


def out_jacs_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_jacs")


def out_mats_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_mats")


@shell.define(
    xor=[["encoding_direction", "encoding_file"], ["encoding_file", "readout_times"]]
)
class TOPUP(shell.Task["TOPUP.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.epi.topup import TOPUP
    >>> from pydra.utils.typing import MultiInputObj

    >>> task = TOPUP()
    >>> task.in_file = Nifti1.mock("b0_b0rev.nii")
    >>> task.encoding_file = File.mock()
    >>> task.cmdline
    'topup --config=b02b0.cnf --datain=topup_encoding.txt --imain=b0_b0rev.nii --out=b0_b0rev_base --iout=b0_b0rev_corrected.nii.gz --fout=b0_b0rev_field.nii.gz --jacout=jac --logout=b0_b0rev_topup.log --rbmout=xfm --dfout=warpfield'


    """

    executable = "topup"
    in_file: Nifti1 = shell.arg(
        help="name of 4D file with images", argstr="--imain={in_file}"
    )
    encoding_file: File | None = shell.arg(
        help="name of text file with PE directions/times",
        argstr="--datain={encoding_file}",
    )
    encoding_direction: list[ty.Any] = shell.arg(
        help="encoding direction for automatic generation of encoding_file",
        requires=["readout_times"],
        formatter=encoding_direction_formatter,
    )
    readout_times: MultiInputObj = shell.arg(
        help="readout times (dwell times by # phase-encode steps minus 1)",
        requires=["encoding_direction"],
    )
    out_base: Path = shell.arg(
        help="base-name of output files (spline coefficients (Hz) and movement parameters)",
        formatter=out_base_formatter,
    )
    out_warp_prefix: str = shell.arg(
        help="prefix for the warpfield images (in mm)",
        argstr="--dfout={out_warp_prefix}",
        default="warpfield",
    )
    out_mat_prefix: str = shell.arg(
        help="prefix for the realignment matrices",
        argstr="--rbmout={out_mat_prefix}",
        default="xfm",
    )
    out_jac_prefix: str = shell.arg(
        help="prefix for the warpfield images",
        argstr="--jacout={out_jac_prefix}",
        default="jac",
    )
    warp_res: float = shell.arg(
        help="(approximate) resolution (in mm) of warp basis for the different sub-sampling levels",
        argstr="--warpres={warp_res}",
    )
    subsamp: int = shell.arg(help="sub-sampling scheme", argstr="--subsamp={subsamp}")
    fwhm: float = shell.arg(
        help="FWHM (in mm) of gaussian smoothing kernel", argstr="--fwhm={fwhm}"
    )
    config: ty.Any = shell.arg(
        help="Name of config file specifying command line arguments",
        argstr="--config={config}",
        default="b02b0.cnf",
    )
    max_iter: int = shell.arg(
        help="max # of non-linear iterations", argstr="--miter={max_iter}"
    )
    reg_lambda: float = shell.arg(
        help="Weight of regularisation, default depending on --ssqlambda and --regmod switches.",
        argstr="--lambda={reg_lambda:0.}",
    )
    ssqlambda: ty.Any = shell.arg(
        help="Weight lambda by the current value of the ssd. If used (=1), the effective weight of regularisation term becomes higher for the initial iterations, therefore initial steps are a little smoother than they would without weighting. This reduces the risk of finding a local minimum.",
        argstr="--ssqlambda={ssqlambda}",
    )
    regmod: ty.Any = shell.arg(
        help="Regularisation term implementation. Defaults to bending_energy. Note that the two functions have vastly different scales. The membrane energy is based on the first derivatives and the bending energy on the second derivatives. The second derivatives will typically be much smaller than the first derivatives, so input lambda will have to be larger for bending_energy to yield approximately the same level of regularisation.",
        argstr="--regmod={regmod}",
    )
    estmov: ty.Any = shell.arg(
        help="estimate movements if set", argstr="--estmov={estmov}"
    )
    minmet: ty.Any = shell.arg(
        help="Minimisation method 0=Levenberg-Marquardt, 1=Scaled Conjugate Gradient",
        argstr="--minmet={minmet}",
    )
    splineorder: int = shell.arg(
        help="order of spline, 2->Qadratic spline, 3->Cubic spline",
        argstr="--splineorder={splineorder}",
    )
    numprec: ty.Any = shell.arg(
        help="Precision for representing Hessian, double or float.",
        argstr="--numprec={numprec}",
    )
    interp: ty.Any = shell.arg(
        help="Image interpolation model, linear or spline.", argstr="--interp={interp}"
    )
    scale: ty.Any = shell.arg(
        help="If set (=1), the images are individually scaled to a common mean",
        argstr="--scale={scale}",
    )
    regrid: ty.Any = shell.arg(
        help="If set (=1), the calculations are done in a different grid",
        argstr="--regrid={regrid}",
    )

    class Outputs(shell.Outputs):
        out_field: Path = shell.outarg(
            help="name of image file with field (Hz)",
            argstr="--fout={out_field}",
            path_template="{in_file}_field",
        )
        out_corrected: Path = shell.outarg(
            help="name of 4D image file with unwarped images",
            argstr="--iout={out_corrected}",
            path_template="{in_file}_corrected",
        )
        out_logfile: Path = shell.outarg(
            help="name of log-file",
            argstr="--logout={out_logfile}",
            path_template="{in_file}_topup.log",
        )
        out_fieldcoef: File | None = shell.out(
            help="file containing the field coefficients",
            callable=out_fieldcoef_callable,
        )
        out_movpar: File | None = shell.out(
            help="movpar.txt output file", callable=out_movpar_callable
        )
        out_enc_file: File | None = shell.out(
            help="encoding directions file output for applytopup",
            callable=out_enc_file_callable,
        )
        out_warps: list[File] | None = shell.out(
            help="warpfield images", callable=out_warps_callable
        )
        out_jacs: list[File] | None = shell.out(
            help="Jacobian images", callable=out_jacs_callable
        )
        out_mats: list[File] | None = shell.out(
            help="realignment matrices", callable=out_mats_callable
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
        msg = "Unable to generate filename for command %s. " % "topup"
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


def _generate_encfile(encoding_direction=None, in_file=None, readout_times=None):
    """Generate a topup compatible encoding file based on given directions"""
    out_file = _get_encfilename(in_file=in_file)
    durations = readout_times
    if len(encoding_direction) != len(durations):
        if len(readout_times) != 1:
            raise ValueError(
                "Readout time must be a float or match the"
                "length of encoding directions"
            )
        durations = durations * len(encoding_direction)

    lines = []
    for idx, encdir in enumerate(encoding_direction):
        direction = 1.0
        if encdir.endswith("-"):
            direction = -1.0
        line = [float(val[0] == encdir[0]) * direction for val in ["x", "y", "z"]] + [
            durations[idx]
        ]
        lines.append(line)
    np.savetxt(out_file, np.array(lines), fmt="%d %d %d %.8f")
    return out_file


def _get_encfilename(
    in_file=None, inputs=None, output_dir=None, stderr=None, stdout=None
):
    out_file = os.path.join(output_dir, ("%s_encfile.txt" % split_filename(in_file)[1]))
    return out_file


IFLOGGER = logging.getLogger("nipype.interface")
