from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input image",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": "1",
        },
    ),
    (
        "new_dims",
        ty.Any,
        {
            "help_string": "3-tuple of new dimension order",
            "argstr": "{new_dims} {new_dims} {new_dims}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "image to write",
            "argstr": "{out_file}",
            "output_file_template": "{in_file}_newdims",
        },
    ),
]
SwapDimensions_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
SwapDimensions_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SwapDimensions(ShellCommandTask):
    input_spec = SwapDimensions_input_spec
    output_spec = SwapDimensions_output_spec
    executable = "fslswapdim"
