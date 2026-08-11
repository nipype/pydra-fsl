import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    if inputs["out_cope"] is not attrs.NOTHING:
        outputs["out_cope"] = os.path.abspath(inputs["out_cope"])

    if inputs["out_z_name"] is not attrs.NOTHING:
        outputs["out_z"] = os.path.abspath(inputs["out_z_name"])

    if inputs["out_t_name"] is not attrs.NOTHING:
        outputs["out_t"] = os.path.abspath(inputs["out_t_name"])

    if inputs["out_p_name"] is not attrs.NOTHING:
        outputs["out_p"] = os.path.abspath(inputs["out_p_name"])

    if inputs["out_f_name"] is not attrs.NOTHING:
        outputs["out_f"] = os.path.abspath(inputs["out_f_name"])

    if inputs["out_pf_name"] is not attrs.NOTHING:
        outputs["out_pf"] = os.path.abspath(inputs["out_pf_name"])

    if inputs["out_res_name"] is not attrs.NOTHING:
        outputs["out_res"] = os.path.abspath(inputs["out_res_name"])

    if inputs["out_varcb_name"] is not attrs.NOTHING:
        outputs["out_varcb"] = os.path.abspath(inputs["out_varcb_name"])

    if inputs["out_sigsq_name"] is not attrs.NOTHING:
        outputs["out_sigsq"] = os.path.abspath(inputs["out_sigsq_name"])

    if inputs["out_data_name"] is not attrs.NOTHING:
        outputs["out_data"] = os.path.abspath(inputs["out_data_name"])

    if inputs["out_vnscales_name"] is not attrs.NOTHING:
        outputs["out_vnscales"] = os.path.abspath(inputs["out_vnscales_name"])

    return outputs


def out_cope_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_cope")


def out_z_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_z")


def out_t_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_t")


def out_p_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_p")


def out_f_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_f")


def out_pf_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_pf")


def out_res_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_res")


def out_varcb_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_varcb")


def out_sigsq_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_sigsq")


def out_data_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_data")


def out_vnscales_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("out_vnscales")


@shell.define
class GLM(shell.Task["GLM.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.model.glm import GLM

    >>> task = GLM()
    >>> task.in_file = Nifti1.mock("functional.nii")
    >>> task.design = Nifti1.mock("maps.nii")
    >>> task.contrasts = File.mock()
    >>> task.mask = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "fsl_glm"
    in_file: Nifti1 = shell.arg(
        help="input file name (text matrix or 3D/4D image file)",
        argstr="-i {in_file}",
        position=1,
    )
    design: Nifti1 = shell.arg(
        help="file name of the GLM design matrix (text time courses for temporal regression or an image file for spatial regression)",
        argstr="-d {design}",
        position=2,
    )
    contrasts: File = shell.arg(
        help="matrix of t-statics contrasts", argstr="-c {contrasts}"
    )
    mask: File = shell.arg(
        help="mask image file name if input is image", argstr="-m {mask}"
    )
    dof: int = shell.arg(help="set degrees of freedom explicitly", argstr="--dof={dof}")
    des_norm: bool = shell.arg(
        help="switch on normalization of the design matrix columns to unit std deviation",
        argstr="--des_norm",
    )
    dat_norm: bool = shell.arg(
        help="switch on normalization of the data time series to unit std deviation",
        argstr="--dat_norm",
    )
    var_norm: bool = shell.arg(
        help="perform MELODIC variance-normalisation on data", argstr="--vn"
    )
    demean: bool = shell.arg(
        help="switch on demeaining of design and data", argstr="--demean"
    )
    out_cope: Path = shell.arg(
        help="output file name for COPE (either as txt or image",
        argstr="--out_cope={out_cope}",
    )
    out_z_name: Path = shell.arg(
        help="output file name for Z-stats (either as txt or image",
        argstr="--out_z={out_z_name}",
    )
    out_t_name: Path = shell.arg(
        help="output file name for t-stats (either as txt or image",
        argstr="--out_t={out_t_name}",
    )
    out_p_name: Path = shell.arg(
        help="output file name for p-values of Z-stats (either as text file or image)",
        argstr="--out_p={out_p_name}",
    )
    out_f_name: Path = shell.arg(
        help="output file name for F-value of full model fit",
        argstr="--out_f={out_f_name}",
    )
    out_pf_name: Path = shell.arg(
        help="output file name for p-value for full model fit",
        argstr="--out_pf={out_pf_name}",
    )
    out_res_name: Path = shell.arg(
        help="output file name for residuals", argstr="--out_res={out_res_name}"
    )
    out_varcb_name: Path = shell.arg(
        help="output file name for variance of COPEs",
        argstr="--out_varcb={out_varcb_name}",
    )
    out_sigsq_name: Path = shell.arg(
        help="output file name for residual noise variance sigma-square",
        argstr="--out_sigsq={out_sigsq_name}",
    )
    out_data_name: Path = shell.arg(
        help="output file name for pre-processed data",
        argstr="--out_data={out_data_name}",
    )
    out_vnscales_name: Path = shell.arg(
        help="output file name for scaling factors for variance normalisation",
        argstr="--out_vnscales={out_vnscales_name}",
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="filename for GLM parameter estimates (GLM betas)",
            argstr="-o {out_file}",
            position=3,
            path_template="{in_file}_glm",
        )
        out_cope: list[File] | None = shell.out(
            help="output file name for COPEs (either as text file or image)",
            callable=out_cope_callable,
        )
        out_z: list[File] | None = shell.out(
            help="output file name for COPEs (either as text file or image)",
            callable=out_z_callable,
        )
        out_t: list[File] | None = shell.out(
            help="output file name for t-stats (either as text file or image)",
            callable=out_t_callable,
        )
        out_p: list[File] | None = shell.out(
            help="output file name for p-values of Z-stats (either as text file or image)",
            callable=out_p_callable,
        )
        out_f: list[File] | None = shell.out(
            help="output file name for F-value of full model fit",
            callable=out_f_callable,
        )
        out_pf: list[File] | None = shell.out(
            help="output file name for p-value for full model fit",
            callable=out_pf_callable,
        )
        out_res: list[File] | None = shell.out(
            help="output file name for residuals", callable=out_res_callable
        )
        out_varcb: list[File] | None = shell.out(
            help="output file name for variance of COPEs", callable=out_varcb_callable
        )
        out_sigsq: list[File] | None = shell.out(
            help="output file name for residual noise variance sigma-square",
            callable=out_sigsq_callable,
        )
        out_data: list[File] | None = shell.out(
            help="output file for preprocessed data", callable=out_data_callable
        )
        out_vnscales: list[File] | None = shell.out(
            help="output file name for scaling factors for variance normalisation",
            callable=out_vnscales_callable,
        )
