import attrs
from fileformats.generic import File
import logging
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

    if name == "local_max_file":
        if isinstance(value, bool):
            return argstr.format(**{name: _list_outputs()["local_max_file"]})

    return argstr.format(**inputs)


def local_max_file_formatter(field, inputs):
    return _format_arg(
        "local_max_file", field, inputs, argstr="--localmax={local_max_file}"
    )


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)
    self_dict = {}

    outputs = {}
    _si = self_dict["inputs"]
    outputs["distance_map"] = _si.distance_map
    if _si.distance_map is attrs.NOTHING:
        outputs["distance_map"] = fname_presuffix(
            _si.in_file, suffix="_dstmap", use_ext=True, newpath=os.getcwd()
        )
    outputs["distance_map"] = os.path.abspath(outputs["distance_map"])
    if _si.local_max_file is not attrs.NOTHING:
        outputs["local_max_file"] = _si.local_max_file
        if isinstance(_si.local_max_file, bool):
            outputs["local_max_file"] = fname_presuffix(
                _si.in_file, suffix="_lclmax", use_ext=True, newpath=os.getcwd()
            )
        outputs["local_max_file"] = os.path.abspath(outputs["local_max_file"])
    return outputs


def local_max_file_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("local_max_file")


def _gen_filename(name, inputs):
    if name == "distance_map":
        return _list_outputs()["distance_map"]
    return None


def distance_map_default(inputs):
    return _gen_filename("distance_map", inputs=inputs)


@shell.define
class DistanceMap(shell.Task["DistanceMap.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pathlib import Path
    >>> from pydra.tasks.fsl.v6.dti.distance_map import DistanceMap

    """

    executable = "distancemap"
    in_file: File = shell.arg(
        help="image to calculate distance values for", argstr="--in={in_file}"
    )
    mask_file: File = shell.arg(
        help="binary mask to constrain calculations", argstr="--mask={mask_file}"
    )
    invert_input: bool = shell.arg(help="invert input image", argstr="--invert")
    local_max_file: ty.Any = shell.arg(
        help="write an image of the local maxima", formatter=local_max_file_formatter
    )

    class Outputs(shell.Outputs):
        distance_map: Path = shell.outarg(
            help="distance map to write",
            argstr="--out={distance_map}",
            path_template="distance_map",
        )
        local_max_file: File | None = shell.out(
            help="image of local maxima", callable=local_max_file_callable
        )
