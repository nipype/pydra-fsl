import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    if inputs["exfdw"] is attrs.NOTHING:
        outputs["exfdw"] = _gen_filename(
            "exfdw",
            epi_file=inputs["epi_file"],
            exf_file=inputs["exf_file"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    else:
        outputs["exfdw"] = inputs["exfdw"]
    if inputs["epi_file"] is not attrs.NOTHING:
        if inputs["epidw"] is not attrs.NOTHING:
            outputs["unwarped_file"] = inputs["epidw"]
        else:
            outputs["unwarped_file"] = _gen_filename(
                "epidw",
                epi_file=inputs["epi_file"],
                exf_file=inputs["exf_file"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
    if inputs["vsm"] is attrs.NOTHING:
        outputs["vsm_file"] = _gen_filename(
            "vsm",
            epi_file=inputs["epi_file"],
            exf_file=inputs["exf_file"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    else:
        outputs["vsm_file"] = _gen_fname(
            inputs["vsm"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    if inputs["tmpdir"] is attrs.NOTHING:
        outputs["exf_mask"] = _gen_fname(
            cwd=_gen_filename(
                "tmpdir",
                epi_file=inputs["epi_file"],
                exf_file=inputs["exf_file"],
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            ),
            basename="maskexf",
        )
    else:
        outputs["exf_mask"] = _gen_fname(
            cwd=inputs["tmpdir"],
            basename="maskexf",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    return outputs


def unwarped_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("unwarped_file")


def vsm_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vsm_file")


def exf_mask_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("exf_mask")


def _gen_filename(name, inputs):
    if name == "exfdw":
        if inputs["exf_file"] is not attrs.NOTHING:
            return _gen_fname(
                inputs["exf_file"], suffix="_exfdw", output_type=inputs["output_type"]
            )
        else:
            return _gen_fname("exfdw", output_type=inputs["output_type"])
    if name == "epidw":
        if inputs["epi_file"] is not attrs.NOTHING:
            return _gen_fname(
                inputs["epi_file"], suffix="_epidw", output_type=inputs["output_type"]
            )
    if name == "vsm":
        return _gen_fname("vsm", output_type=inputs["output_type"])
    if name == "tmpdir":
        return os.path.join(os.getcwd(), "temp")
    return None


def exfdw_default(inputs):
    return _gen_filename("exfdw", inputs=inputs)


def tmpdir_default(inputs):
    return _gen_filename("tmpdir", inputs=inputs)


def vsm_default(inputs):
    return _gen_filename("vsm", inputs=inputs)


@shell.define
class EPIDeWarp(shell.Task["EPIDeWarp.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pydra.tasks.fsl.v6.epi.epi_de_warp import EPIDeWarp

    >>> task = EPIDeWarp()
    >>> task.mag_file = File.mock()
    >>> task.dph_file = Nifti1.mock("phase.nii")
    >>> task.exf_file = File.mock()
    >>> task.epi_file = Nifti1.mock("functional.nii")
    >>> task.cmdline
    'epidewarp.fsl --mag magnitude.nii --dph phase.nii --epi functional.nii --esp 0.58 --exfdw .../exfdw.nii.gz --nocleanup --sigma 2 --tediff 2.46 --tmpdir .../temp --vsm .../vsm.nii.gz'


    """

    executable = "epidewarp.fsl"
    mag_file: File = shell.arg(
        help="Magnitude file", argstr="--mag {mag_file}", position=1
    )
    dph_file: Nifti1 = shell.arg(
        help="Phase file assumed to be scaled from 0 to 4095", argstr="--dph {dph_file}"
    )
    exf_file: File = shell.arg(
        help="example func volume (or use epi)", argstr="--exf {exf_file}"
    )
    epi_file: Nifti1 = shell.arg(help="EPI volume to unwarp", argstr="--epi {epi_file}")
    tediff: float = shell.arg(
        help="difference in B0 field map TEs", argstr="--tediff {tediff}", default=2.46
    )
    esp: float = shell.arg(help="EPI echo spacing", argstr="--esp {esp}", default=0.58)
    sigma: int = shell.arg(
        help="2D spatial gaussing smoothing                        stdev (default = 2mm)",
        argstr="--sigma {sigma}",
        default=2,
    )
    vsm: ty.Any = shell.arg(help="voxel shift map", argstr="--vsm {vsm}")
    epidw: ty.Any = shell.arg(help="dewarped epi volume", argstr="--epidw {epidw}")
    tmpdir: ty.Any = shell.arg(help="tmpdir", argstr="--tmpdir {tmpdir}")
    nocleanup: bool = shell.arg(help="no cleanup", argstr="--nocleanup", default=True)
    cleanup: bool = shell.arg(help="cleanup", argstr="--cleanup")

    class Outputs(shell.Outputs):
        exfdw: ty.Any = shell.outarg(
            help="dewarped example func volume",
            argstr="--exfdw {exfdw}",
            path_template="exfdw",
        )
        unwarped_file: File | None = shell.out(
            help="unwarped epi file", callable=unwarped_file_callable
        )
        vsm_file: File | None = shell.out(
            help="voxel shift map", callable=vsm_file_callable
        )
        exf_mask: File | None = shell.out(
            help="Mask from example functional volume", callable=exf_mask_callable
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
        msg = "Unable to generate filename for command %s. " % "epidewarp.fsl"
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


IFLOGGER = logging.getLogger("nipype.interface")
