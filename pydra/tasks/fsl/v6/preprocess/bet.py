import attrs
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import fname_presuffix
import os
import os.path as op
from pathlib import Path
from pathlib import Path
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _format_arg(name, value, inputs, argstr):
    if value is None:
        return ""

    formatted = argstr.format(**inputs)
    if name == "in_file":

        return op.relpath(formatted, start=os.getcwd())
    return formatted

    return argstr.format(**inputs)


def in_file_formatter(field, inputs):
    return _format_arg("in_file", field, inputs, argstr="{in_file}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}
    outputs["out_file"] = os.path.abspath(
        _gen_outfilename(
            in_file=inputs["in_file"],
            out_file=inputs["out_file"],
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
        )
    )

    basename = os.path.basename(outputs["out_file"])
    cwd = os.path.dirname(outputs["out_file"])
    kwargs = {"basename": basename, "cwd": cwd}

    if ((inputs["mesh"] is not attrs.NOTHING) and inputs["mesh"]) or (
        (inputs["surfaces"] is not attrs.NOTHING) and inputs["surfaces"]
    ):
        outputs["meshfile"] = _gen_fname(
            suffix="_mesh.vtk",
            change_ext=False,
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
    if ((inputs["mask"] is not attrs.NOTHING) and inputs["mask"]) or (
        (inputs["reduce_bias"] is not attrs.NOTHING) and inputs["reduce_bias"]
    ):
        outputs["mask_file"] = _gen_fname(
            suffix="_mask",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
    if (inputs["outline"] is not attrs.NOTHING) and inputs["outline"]:
        outputs["outline_file"] = _gen_fname(
            suffix="_overlay",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
    if (inputs["surfaces"] is not attrs.NOTHING) and inputs["surfaces"]:
        outputs["inskull_mask_file"] = _gen_fname(
            suffix="_inskull_mask",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["inskull_mesh_file"] = _gen_fname(
            suffix="_inskull_mesh",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["outskull_mask_file"] = _gen_fname(
            suffix="_outskull_mask",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["outskull_mesh_file"] = _gen_fname(
            suffix="_outskull_mesh",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["outskin_mask_file"] = _gen_fname(
            suffix="_outskin_mask",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["outskin_mesh_file"] = _gen_fname(
            suffix="_outskin_mesh",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
        outputs["skull_mask_file"] = _gen_fname(
            suffix="_skull_mask",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
    if (inputs["skull"] is not attrs.NOTHING) and inputs["skull"]:
        outputs["skull_file"] = _gen_fname(
            suffix="_skull",
            output_type=inputs["output_type"],
            inputs=inputs["inputs"],
            output_dir=inputs["output_dir"],
            stderr=inputs["stderr"],
            stdout=inputs["stdout"],
            **kwargs,
        )
    if (inputs["no_output"] is not attrs.NOTHING) and inputs["no_output"]:
        outputs["out_file"] = type(attrs.NOTHING)
    return outputs


def mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("mask_file")


def outline_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("outline_file")


def meshfile_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("meshfile")


def inskull_mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("inskull_mask_file")


def inskull_mesh_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("inskull_mesh_file")


def outskull_mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("outskull_mask_file")


def outskull_mesh_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("outskull_mesh_file")


def outskin_mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("outskin_mask_file")


def outskin_mesh_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("outskin_mesh_file")


def skull_mask_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("skull_mask_file")


def skull_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("skull_file")


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


@shell.define(
    xor=[
        [
            "functional",
            "padding",
            "reduce_bias",
            "remove_eyes",
            "robust",
            "surfaces",
            "t2_guided",
        ]
    ]
)
class BET(shell.Task["BET.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from fileformats.medimage import Nifti1
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.bet import BET

    >>> task = BET()
    >>> task.in_file = Nifti1.mock("structural.nii")
    >>> task.out_file = "brain_anat.nii"
    >>> task.t2_guided = File.mock()
    >>> task.cmdline
    'None'


    """

    executable = "bet"
    in_file: Nifti1 = shell.arg(
        help="input file to skull strip", formatter=in_file_formatter, position=1
    )
    outline: bool = shell.arg(help="create surface outline image", argstr="-o")
    mask: bool = shell.arg(help="create binary mask image", argstr="-m")
    skull: bool = shell.arg(help="create skull image", argstr="-s")
    no_output: bool = shell.arg(help="Don't generate segmented output", argstr="-n")
    frac: float = shell.arg(
        help="fractional intensity threshold", argstr="-f {frac:.2}"
    )
    vertical_gradient: float = shell.arg(
        help="vertical gradient in fractional intensity threshold (-1, 1)",
        argstr="-g {vertical_gradient:.2}",
    )
    radius: int = shell.arg(help="head radius", argstr="-r {radius}")
    center: list[int] = shell.arg(
        help="center of gravity in voxels", argstr="-c {center}"
    )
    threshold: bool = shell.arg(
        help="apply thresholding to segmented brain image and mask", argstr="-t"
    )
    mesh: bool = shell.arg(help="generate a vtk mesh brain surface", argstr="-e")
    robust: bool = shell.arg(
        help="robust brain centre estimation (iterates BET several times)", argstr="-R"
    )
    padding: bool = shell.arg(
        help="improve BET if FOV is very small in Z (by temporarily padding end slices)",
        argstr="-Z",
    )
    remove_eyes: bool = shell.arg(
        help="eye & optic nerve cleanup (can be useful in SIENA)", argstr="-S"
    )
    surfaces: bool = shell.arg(
        help="run bet2 and then betsurf to get additional skull and scalp surfaces (includes registrations)",
        argstr="-A",
    )
    t2_guided: File | None = shell.arg(
        help="as with creating surfaces, when also feeding in non-brain-extracted T2 (includes registrations)",
        argstr="-A2 {t2_guided}",
    )
    functional: bool = shell.arg(help="apply to 4D fMRI data", argstr="-F")
    reduce_bias: bool = shell.arg(help="bias field and neck cleanup", argstr="-B")

    class Outputs(shell.Outputs):
        out_file: Path = shell.outarg(
            help="name of output skull stripped image",
            argstr="{out_file}",
            path_template='"brain_anat.nii"',
            position=2,
        )
        mask_file: File | None = shell.out(
            help="path/name of binary brain mask (if generated)",
            callable=mask_file_callable,
        )
        outline_file: File | None = shell.out(
            help="path/name of outline file (if generated)",
            callable=outline_file_callable,
        )
        meshfile: File | None = shell.out(
            help="path/name of vtk mesh file (if generated)", callable=meshfile_callable
        )
        inskull_mask_file: File | None = shell.out(
            help="path/name of inskull mask (if generated)",
            callable=inskull_mask_file_callable,
        )
        inskull_mesh_file: File | None = shell.out(
            help="path/name of inskull mesh outline (if generated)",
            callable=inskull_mesh_file_callable,
        )
        outskull_mask_file: File | None = shell.out(
            help="path/name of outskull mask (if generated)",
            callable=outskull_mask_file_callable,
        )
        outskull_mesh_file: File | None = shell.out(
            help="path/name of outskull mesh outline (if generated)",
            callable=outskull_mesh_file_callable,
        )
        outskin_mask_file: File | None = shell.out(
            help="path/name of outskin mask (if generated)",
            callable=outskin_mask_file_callable,
        )
        outskin_mesh_file: File | None = shell.out(
            help="path/name of outskin mesh outline (if generated)",
            callable=outskin_mesh_file_callable,
        )
        skull_mask_file: File | None = shell.out(
            help="path/name of skull mask (if generated)",
            callable=skull_mask_file_callable,
        )
        skull_file: File | None = shell.out(
            help="path/name of skull file (if generated)", callable=skull_file_callable
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
        msg = "Unable to generate filename for command %s. " % "bet"
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

    if (out_file is attrs.NOTHING) and (in_file is not attrs.NOTHING):
        out_file = _gen_fname(in_file, suffix="_brain", output_type=output_type)

        return op.relpath(out_file, start=output_dir)
    return out_file


IFLOGGER = logging.getLogger("nipype.interface")
