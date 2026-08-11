import attrs
from fileformats.generic import File
import logging
from pydra.tasks.fsl.v6.nipype_ports.utils.filemanip import split_filename
import os.path as op
from pathlib import Path
from pathlib import Path
from pydra.compose import shell
import typing as ty


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    outputs = {}

    if inputs["list_of_specific_structures"] is not attrs.NOTHING:
        structures = inputs["list_of_specific_structures"]
    else:
        structures = [
            "L_Hipp",
            "R_Hipp",
            "L_Accu",
            "R_Accu",
            "L_Amyg",
            "R_Amyg",
            "L_Caud",
            "R_Caud",
            "L_Pall",
            "R_Pall",
            "L_Puta",
            "R_Puta",
            "L_Thal",
            "R_Thal",
            "BrStem",
        ]
    outputs["original_segmentations"] = _gen_fname(
        "original_segmentations",
        list_of_specific_structures=inputs["list_of_specific_structures"],
        method=inputs["method"],
        method_as_numerical_threshold=inputs["method_as_numerical_threshold"],
        out_file=inputs["out_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["segmentation_file"] = _gen_fname(
        "segmentation_file",
        list_of_specific_structures=inputs["list_of_specific_structures"],
        method=inputs["method"],
        method_as_numerical_threshold=inputs["method_as_numerical_threshold"],
        out_file=inputs["out_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["vtk_surfaces"] = _gen_mesh_names(
        "vtk_surfaces",
        structures,
        out_file=inputs["out_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    outputs["bvars"] = _gen_mesh_names(
        "bvars",
        structures,
        out_file=inputs["out_file"],
        inputs=inputs["inputs"],
        output_dir=inputs["output_dir"],
        stderr=inputs["stderr"],
        stdout=inputs["stdout"],
    )
    return outputs


def vtk_surfaces_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("vtk_surfaces")


def bvars_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("bvars")


def original_segmentations_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("original_segmentations")


def segmentation_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("segmentation_file")


@shell.define(xor=[["method", "method_as_numerical_threshold"]])
class FIRST(shell.Task["FIRST.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.preprocess.first import FIRST

    """

    executable = "run_first_all"
    in_file: File = shell.arg(
        help="input data file", argstr="-i {in_file}", position=-2
    )
    out_file: Path | None = shell.arg(
        help="output data file",
        argstr="-o {out_file}",
        position=-1,
        default="segmented",
    )
    verbose: bool = shell.arg(help="Use verbose logging.", argstr="-v", position=1)
    brain_extracted: bool = shell.arg(
        help="Input structural image is already brain-extracted",
        argstr="-b",
        position=2,
    )
    no_cleanup: bool = shell.arg(
        help="Input structural image is already brain-extracted",
        argstr="-d",
        position=3,
    )
    method: ty.Any | None = shell.arg(
        help="Method must be one of auto, fast, none, or it can be entered using the 'method_as_numerical_threshold' input",
        argstr="-m {method}",
        position=4,
        default="auto",
    )
    method_as_numerical_threshold: float | None = shell.arg(
        help="Specify a numerical threshold value or use the 'method' input to choose auto, fast, or none",
        argstr="-m {method_as_numerical_threshold:.4}",
        position=4,
    )
    list_of_specific_structures: list[str] = shell.arg(
        help="Runs only on the specified structures (e.g. L_Hipp, R_HippL_Accu, R_Accu, L_Amyg, R_AmygL_Caud, R_Caud, L_Pall, R_PallL_Puta, R_Puta, L_Thal, R_Thal, BrStem",
        argstr="-s {list_of_specific_structures}",
        position=5,
        sep=",",
    )
    affine_file: File = shell.arg(
        help="Affine matrix to use (e.g. img2std.mat) (does not re-run registration)",
        argstr="-a {affine_file}",
        position=6,
    )

    class Outputs(shell.Outputs):
        vtk_surfaces: list[File] | None = shell.out(
            help="VTK format meshes for each subcortical region",
            callable=vtk_surfaces_callable,
        )
        bvars: list[File] | None = shell.out(
            help="bvars for each subcortical region", callable=bvars_callable
        )
        original_segmentations: File | None = shell.out(
            help="3D image file containing the segmented regions as integer values. Uses CMA labelling",
            callable=original_segmentations_callable,
        )
        segmentation_file: File | None = shell.out(
            help="4D image file containing a single volume per segmented region",
            callable=segmentation_file_callable,
        )


def _gen_fname(
    basename,
    list_of_specific_structures=None,
    method=None,
    method_as_numerical_threshold=None,
    out_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    path, outname, ext = split_filename(out_file)

    method = "none"
    if (method is not attrs.NOTHING) and method != "none":
        method = "fast"
        if list_of_specific_structures and method == "auto":
            method = "none"

    if method_as_numerical_threshold is not attrs.NOTHING:
        thres = "%.4f" % method_as_numerical_threshold
        method = thres.replace(".", "")

    if basename == "original_segmentations":
        return op.abspath(f"{outname}_all_{method}_origsegs.nii.gz")
    if basename == "segmentation_file":
        return op.abspath(f"{outname}_all_{method}_firstseg.nii.gz")

    return None


def _gen_mesh_names(
    name,
    structures,
    out_file=None,
    inputs=None,
    output_dir=None,
    stderr=None,
    stdout=None,
):
    path, prefix, ext = split_filename(out_file)
    if name == "vtk_surfaces":
        vtks = list()
        for struct in structures:
            vtk = prefix + "-" + struct + "_first.vtk"
            vtks.append(op.abspath(vtk))
        return vtks
    if name == "bvars":
        bvars = list()
        for struct in structures:
            bvar = prefix + "-" + struct + "_first.bvars"
            bvars.append(op.abspath(bvar))
        return bvars
    return None
