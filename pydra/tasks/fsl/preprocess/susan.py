from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "{in_file}",
            "help_string": "filename of input timeseries",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "brightness_threshold",
        float,
        {
            "argstr": "{brightness_threshold:.10f}",
            "help_string": "brightness threshold and should be greater than noise level and less than contrast of edges to be preserved.",
            "mandatory": True,
            "position": 2,
        },
    ),
    (
        "fwhm",
        float,
        {
            "argstr": "{fwhm:.10f}",
            "help_string": "fwhm of smoothing, in mm, gets converted using sqrt(8*log(2))",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "dimension",
        ty.Any,
        3,
        {
            "argstr": "{dimension}",
            "help_string": "within-plane (2) or fully 3D (3)",
            "position": 4,
        },
    ),
    (
        "use_median",
        ty.Any,
        1,
        {
            "argstr": "{use_median}",
            "help_string": "whether to use a local median filter in the cases where single-point noise is detected",
            "position": 5,
        },
    ),
    (
        "usans",
        list,
        [],
        {
            "argstr": "",
            "help_string": "determines whether the smoothing area (USAN) is to be found from secondary images (0, 1 or 2). A negative value for any brightness threshold will auto-set the threshold at 10% of the robust range",
            "position": 6,
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "{out_file}",
            "help_string": "output file name",
            "position": -1,
            "output_file_template": "{in_file}_smooth",
        },
    ),
]
SUSAN_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "smoothed_file",
        specs.File,
        {
            "help_string": "smoothed output file",
            "requires": ["out_file"],
            "output_file_template": "{out_file}",
        },
    )
]
SUSAN_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SUSAN(ShellCommandTask):
    input_spec = SUSAN_input_spec
    output_spec = SUSAN_output_spec
    executable = "susan"
