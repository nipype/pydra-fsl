import attrs
from fileformats.generic import File
import logging
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
    self_dict = {}

    if name == "project_data":
        if (value is not attrs.NOTHING) and value:
            _si = self_dict["inputs"]
            if (_si.use_cingulum_mask is not attrs.NOTHING) and _si.use_cingulum_mask:
                mask_file = Info.standard_image("LowerCingulum_1mm.nii.gz")
            else:
                mask_file = _si.search_mask_file
            if _si.projected_data is attrs.NOTHING:
                proj_file = _list_outputs()["projected_data"]
            else:
                proj_file = _si.projected_data
            return argstr % (
                _si.threshold,
                _si.distance_map,
                mask_file,
                _si.data_file,
                proj_file,
            )
    elif name == "skeleton_file":
        if isinstance(value, bool):
            return argstr.format(**{name: _list_outputs()["skeleton_file"]})
        else:
            return argstr.format(**{name: value})

    return argstr.format(**inputs)


def project_data_formatter(field, inputs):
    return _format_arg(
        "project_data",
        field,
        inputs,
        argstr="-p {project_data:d:.3} {project_data:d} {project_data:d} {project_data:d} {project_data:d}",
    )


def skeleton_file_formatter(field, inputs):
    return _format_arg("skeleton_file", field, inputs, argstr="-o {skeleton_file}")


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    _si = self_dict["inputs"]
    if (_si.project_data is not attrs.NOTHING) and _si.project_data:
        proj_data = _si.projected_data
        outputs["projected_data"] = proj_data
        if proj_data is attrs.NOTHING:
            stem = _si.data_file
            if _si.alt_data_file is not attrs.NOTHING:
                stem = _si.alt_data_file
            outputs["projected_data"] = fname_presuffix(
                stem, suffix="_skeletonised", newpath=os.getcwd(), use_ext=True
            )
    if (_si.skeleton_file is not attrs.NOTHING) and _si.skeleton_file:
        outputs["skeleton_file"] = _si.skeleton_file
        if isinstance(_si.skeleton_file, bool):
            outputs["skeleton_file"] = fname_presuffix(
                _si.in_file, suffix="_skeleton", newpath=os.getcwd(), use_ext=True
            )
    return outputs


def projected_data_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("projected_data")


def skeleton_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("skeleton_file")


@shell.define(xor=[["search_mask_file", "use_cingulum_mask"]])
class TractSkeleton(shell.Task["TractSkeleton.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.dti.tract_skeleton import TractSkeleton

    """

    executable = "tbss_skeleton"
    in_file: File = shell.arg(
        help="input image (typically mean FA volume)", argstr="-i {in_file}"
    )
    project_data: bool = shell.arg(
        help="project data onto skeleton",
        requires=["threshold", "distance_map", "data_file"],
        formatter=project_data_formatter,
    )
    threshold: float = shell.arg(help="skeleton threshold value")
    distance_map: File = shell.arg(help="distance map image")
    search_mask_file: File | None = shell.arg(
        help="mask in which to use alternate search rule"
    )
    use_cingulum_mask: bool = shell.arg(
        help="perform alternate search using built-in cingulum mask", default=True
    )
    data_file: File = shell.arg(help="4D data to project onto skeleton (usually FA)")
    alt_data_file: File = shell.arg(
        help="4D non-FA data to project onto skeleton", argstr="-a {alt_data_file}"
    )
    alt_skeleton: File = shell.arg(
        help="alternate skeleton to use", argstr="-s {alt_skeleton}"
    )
    projected_data: Path = shell.arg(help="input data projected onto skeleton")
    skeleton_file: ty.Any = shell.arg(
        help="write out skeleton image", formatter=skeleton_file_formatter
    )

    class Outputs(shell.Outputs):
        projected_data: File | None = shell.out(
            help="input data projected onto skeleton", callable=projected_data_callable
        )
        skeleton_file: File | None = shell.out(
            help="tract skeleton image", callable=skeleton_file_callable
        )
