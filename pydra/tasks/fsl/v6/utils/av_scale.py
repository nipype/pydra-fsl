import attrs
from fileformats.generic import File
import logging
from pydra.compose import shell


logger = logging.getLogger(__name__)


def _list_outputs(inputs=None, stdout=None, stderr=None, output_dir=None):
    inputs = attrs.asdict(inputs)

    return parsed_inputs["_results"]


def rotation_translation_matrix_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rotation_translation_matrix")


def scales_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("scales")


def skews_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("skews")


def average_scaling_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("average_scaling")


def determinant_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("determinant")


def forward_half_transform_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("forward_half_transform")


def backward_half_transform_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("backward_half_transform")


def left_right_orientation_preserved_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("left_right_orientation_preserved")


def rot_angles_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("rot_angles")


def translations_callable(output_dir, inputs, stdout, stderr):
    outputs = _list_outputs(
        output_dir=output_dir, inputs=inputs, stdout=stdout, stderr=stderr
    )
    return outputs.get("translations")


@shell.define
class AvScale(shell.Task["AvScale.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fsl.v6.utils.av_scale import AvScale

    """

    executable = "avscale"
    all_param: bool = shell.arg(help="", argstr="--allparams")
    mat_file: File = shell.arg(
        help="mat file to read", argstr="{mat_file}", position=-2
    )
    ref_file: File = shell.arg(
        help="reference file to get center of rotation",
        argstr="{ref_file}",
        position=-1,
    )

    class Outputs(shell.Outputs):
        rotation_translation_matrix: list[list[float]] | None = shell.out(
            help="Rotation and Translation Matrix",
            callable=rotation_translation_matrix_callable,
        )
        scales: list[float] | None = shell.out(
            help="Scales (x,y,z)", callable=scales_callable
        )
        skews: list[float] | None = shell.out(help="Skews", callable=skews_callable)
        average_scaling: float | None = shell.out(
            help="Average Scaling", callable=average_scaling_callable
        )
        determinant: float | None = shell.out(
            help="Determinant", callable=determinant_callable
        )
        forward_half_transform: list[list[float]] | None = shell.out(
            help="Forward Half Transform", callable=forward_half_transform_callable
        )
        backward_half_transform: list[list[float]] | None = shell.out(
            help="Backwards Half Transform", callable=backward_half_transform_callable
        )
        left_right_orientation_preserved: bool | None = shell.out(
            help="True if LR orientation preserved",
            callable=left_right_orientation_preserved_callable,
        )
        rot_angles: list[float] | None = shell.out(
            help="rotation angles", callable=rot_angles_callable
        )
        translations: list[float] | None = shell.out(
            help="translations", callable=translations_callable
        )
