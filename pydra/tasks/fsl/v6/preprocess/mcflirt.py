import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from looseversion import LooseVersion
from nibabel import load
from pydra.tasks.fsl.v6.base import Info
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    if name == "interpolation":
        if value == "trilinear":
            return ""
        else:
            return argstr.format(**{name: value})

    return argstr.format(**inputs)


def interpolation_formatter(field, inputs):
    return _format_arg("interpolation", field, inputs, argstr="-{interpolation}_final")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    outputs["out_file"] = _gen_outfilename(
        in_file=inputs["in_file"],
        out_file=inputs["out_file"],
        output_type=inputs["output_type"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    output_dir = os.path.dirname(outputs["out_file"])

    if (inputs["stats_imgs"] is not attrs.NOTHING) and inputs["stats_imgs"]:
        if LooseVersion(Info.version()) < LooseVersion("6.0.0"):

            outputs["variance_img"] = _gen_fname(
                outputs["out_file"] + "_variance.ext",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
            outputs["std_img"] = _gen_fname(
                outputs["out_file"] + "_sigma.ext",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        else:
            outputs["variance_img"] = _gen_fname(
                outputs["out_file"],
                suffix="_variance",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
            outputs["std_img"] = _gen_fname(
                outputs["out_file"],
                suffix="_sigma",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )

    if (inputs["mean_vol"] is not attrs.NOTHING) and inputs["mean_vol"]:
        if LooseVersion(Info.version()) < LooseVersion("6.0.0"):

            outputs["mean_img"] = _gen_fname(
                outputs["out_file"] + "_mean_reg.ext",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )
        else:
            outputs["mean_img"] = _gen_fname(
                outputs["out_file"],
                suffix="_mean_reg",
                cwd=output_dir,
                output_type=inputs["output_type"],
                inputs=inputs["inputs"],
                output_dir=inputs["output_dir"],
                stderr=inputs["stderr"],
                stdout=inputs["stdout"],
            )

    if (inputs["save_mats"] is not attrs.NOTHING) and inputs["save_mats"]:
        _, filename = os.path.split(outputs["out_file"])
        matpathname = os.path.join(output_dir, filename + ".mat")
        _, _, _, timepoints = load(inputs["in_file"]).shape
        outputs["mat_file"] = []
        for t in range(timepoints):
            outputs["mat_file"].append(os.path.join(matpathname, "MAT_%04d" % t))
    if (inputs["save_plots"] is not attrs.NOTHING) and inputs["save_plots"]:

        outputs["par_file"] = outputs["out_file"] + ".par"
    if (inputs["save_rms"] is not attrs.NOTHING) and inputs["save_rms"]:
        outfile = outputs["out_file"]
        outputs["rms_files"] = [outfile + "_abs.rms", outfile + "_rel.rms"]
    return outputs


def variance_img_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("variance_img")


def std_img_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("std_img")


def mean_img_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mean_img")


def par_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("par_file")


def mat_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mat_file")


def rms_files_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rms_files")


def _gen_filename(name, inputs):
    if name == "out_file":
        return _gen_outfilename(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
        )
    return None


def out_file_default(inputs):
    return _gen_filename("out_file", inputs=inputs)


@shell.define
class MCFLIRT(shell.Task["MCFLIRT.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.mcflirt import MCFLIRT

    >>> task = MCFLIRT()
    >>> task.in_file = Nifti1.mock("functional.nii")
    >>> task.out_file = "moco.nii"
    >>> task.init = File.mock()
    >>> task.ref_file = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "mcflirt"
    in_file: Nifti1 = shell.arg(
        help="timeseries to motion-correct", argstr="-in {in_file}", position=1
    )
    cost: ty.Any = shell.arg(help="cost function to optimize", argstr="-cost {cost}")
    bins: int = shell.arg(help="number of histogram bins", argstr="-bins {bins}")
    dof: int = shell.arg(
        help="degrees of freedom for the transformation", argstr="-dof {dof}"
    )
    ref_vol: int = shell.arg(
        help="volume to align frames to", argstr="-refvol {ref_vol}"
    )
    scaling: float = shell.arg(
        help="scaling factor to use", argstr="-scaling {scaling:.2}"
    )
    smooth: float = shell.arg(
        help="smoothing factor for the cost function", argstr="-smooth {smooth:.2}"
    )
    rotation: int = shell.arg(
        help="scaling factor for rotation tolerances", argstr="-rotation {rotation}"
    )
    stages: int = shell.arg(
        help="stages (if 4, perform final search with sinc interpolation",
        argstr="-stages {stages}",
    )
    init: File = shell.arg(help="initial transformation matrix", argstr="-init {init}")
    interpolation: ty.Any = shell.arg(
        help="interpolation method for transformation",
        formatter=interpolation_formatter,
    )
    use_gradient: bool = shell.arg(help="run search on gradient images", argstr="-gdt")
    use_contour: bool = shell.arg(help="run search on contour images", argstr="-edge")
    mean_vol: bool = shell.arg(help="register to mean volume", argstr="-meanvol")
    stats_imgs: bool = shell.arg(
        help="produce variance and std. dev. images", argstr="-stats"
    )
    save_mats: bool = shell.arg(help="save transformation matrices", argstr="-mats")
    save_plots: bool = shell.arg(help="save transformation parameters", argstr="-plots")
    save_rms: bool = shell.arg(
        help="save rms displacement parameters", argstr="-rmsabs -rmsrel"
    )
    ref_file: File = shell.arg(
        help="target image for motion correction", argstr="-reffile {ref_file}"
    )

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="file to write", argstr="-out {out_file}", path_template='"moco.nii"'
        )
        variance_img: File | None = shell.out(
            help="variance image", callable=variance_img_callable
        )
        std_img: File | None = shell.out(
            help="standard deviation image", callable=std_img_callable
        )
        mean_img: File | None = shell.out(
            help="mean timeseries image (if mean_vol=True)", callable=mean_img_callable
        )
        par_file: File | None = shell.out(
            help="text-file with motion parameters", callable=par_file_callable
        )
        mat_file: list[File] | None = shell.out(
            help="transformation matrices", callable=mat_file_callable
        )
        rms_files: list[File] | None = shell.out(
            help="absolute and relative displacement parameters",
            callable=rms_files_callable,
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
        msg = "Unable to generate filename for command %s. " % "mcflirt"
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


def _gen_outfilename(
    in_file=None,
    out_file=None,
    output_type=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    out_file = out_file
    if out_file is not attrs.NOTHING:
        out_file = os.path.realpath(out_file)
    if (out_file is attrs.NOTHING) and (in_file is not attrs.NOTHING):
        out_file = _gen_fname(in_file, suffix="_mcf", output_type=output_type)
    return os.path.abspath(out_file)


IFLOGGER = logging.getLogger("nipype.interface")
