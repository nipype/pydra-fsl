from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def Complex_output(inputs):
    import attr

    if inputs.complex_cartesian:
        in_file = inputs.real_in_file
    elif inputs.complex_polar:
        in_file = inputs.magnitude_in_file
    elif inputs.complex_split or inputs.complex_merge:
        in_file = inputs.complex_in_file
    else:
        return None
    return f"{in_file}_cplx"


input_fields = [
    (
        "complex_in_file",
        specs.File,
        {"help_string": "", "argstr": "{complex_in_file}", "position": 2},
    ),
    (
        "complex_in_file2",
        specs.File,
        {"help_string": "", "argstr": "{complex_in_file2}", "position": 3},
    ),
    (
        "real_in_file",
        specs.File,
        {"help_string": "", "argstr": "{real_in_file}", "position": 2},
    ),
    (
        "imaginary_in_file",
        specs.File,
        {"help_string": "", "argstr": "{imaginary_in_file}", "position": 3},
    ),
    (
        "magnitude_in_file",
        specs.File,
        {"help_string": "", "argstr": "{magnitude_in_file}", "position": 2},
    ),
    (
        "phase_in_file",
        specs.File,
        {"help_string": "", "argstr": "{phase_in_file}", "position": 3},
    ),
    (
        "complex_out_file",
        str,
        {
            "help_string": "",
            "argstr": "{complex_out_file}",
            "position": -3,
            "xor": [
                "complex_out_file",
                "magnitude_out_file",
                "phase_out_file",
                "real_out_file",
                "imaginary_out_file",
                "real_polar",
                "real_cartesian",
            ],
        },
    ),
    (
        "magnitude_out_file",
        str,
        {
            "help_string": "",
            "argstr": "{magnitude_out_file}",
            "position": -4,
            "xor": [
                "complex_out_file",
                "real_out_file",
                "imaginary_out_file",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
            "output_file_template": "{in_file}_mag",
        },
    ),
    (
        "phase_out_file",
        str,
        {
            "help_string": "",
            "argstr": "{phase_out_file}",
            "position": -3,
            "xor": [
                "complex_out_file",
                "real_out_file",
                "imaginary_out_file",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
            "output_file_template": "{in_file}_phase",
        },
    ),
    (
        "real_out_file",
        str,
        {
            "help_string": "",
            "argstr": "{real_out_file}",
            "position": -4,
            "xor": [
                "complex_out_file",
                "magnitude_out_file",
                "phase_out_file",
                "real_polar",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
            "output_file_template": "{in_file}_real",
        },
    ),
    (
        "imaginary_out_file",
        str,
        {
            "help_string": "",
            "argstr": "{imaginary_out_file}",
            "position": -3,
            "xor": [
                "complex_out_file",
                "magnitude_out_file",
                "phase_out_file",
                "real_polar",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
            "output_file_template": "{in_file}_imag",
        },
    ),
    ("start_vol", int, {"help_string": "", "argstr": "{start_vol}", "position": -2}),
    ("end_vol", int, {"help_string": "", "argstr": "{end_vol}", "position": -1}),
    (
        "real_polar",
        bool,
        {
            "help_string": "",
            "argstr": "-realpolar",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
        },
    ),
    (
        "real_cartesian",
        bool,
        {
            "help_string": "",
            "argstr": "-realcartesian",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
        },
    ),
    (
        "complex_cartesian",
        bool,
        {
            "help_string": "",
            "argstr": "-complex",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
        },
    ),
    (
        "complex_polar",
        bool,
        {
            "help_string": "",
            "argstr": "-complexpolar",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
        },
    ),
    (
        "complex_split",
        bool,
        {
            "help_string": "",
            "argstr": "-complexsplit",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
            ],
        },
    ),
    (
        "complex_merge",
        bool,
        {
            "help_string": "",
            "argstr": "-complexmerge",
            "position": 1,
            "xor": [
                "real_polar",
                "real_cartesian",
                "complex_cartesian",
                "complex_polar",
                "complex_split",
                "complex_merge",
                "start_vol",
                "end_vol",
            ],
        },
    ),
]
Complex_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
Complex_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Complex(ShellCommandTask):
    input_spec = Complex_input_spec
    output_spec = Complex_output_spec
    executable = "fslcomplex"
