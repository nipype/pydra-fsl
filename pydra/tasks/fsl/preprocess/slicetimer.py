from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "--in={in_file}",
            "help_string": "filename of input timeseries",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "--out={out_file}",
            "help_string": "filename of output timeseries",
            "output_file_template": "{in_file}_st",
        },
    ),
    (
        "index_dir",
        bool,
        {"argstr": "--down", "help_string": "slice indexing from top to bottom"},
    ),
    (
        "time_repetition",
        float,
        {
            "argstr": "--repeat={time_repetition}",
            "help_string": "Specify TR of data - default is 3s",
        },
    ),
    (
        "slice_direction",
        ty.Any,
        {
            "argstr": "--direction={slice_direction}",
            "help_string": "direction of slice acquisition (x=1, y=2, z=3) - default is z",
        },
    ),
    (
        "interleaved",
        bool,
        {"argstr": "--odd", "help_string": "use interleaved acquisition"},
    ),
    (
        "custom_timings",
        specs.File,
        {
            "argstr": "--tcustom={custom_timings}",
            "help_string": "slice timings, in fractions of TR, range 0:1 (default is 0.5 = no shift)",
        },
    ),
    (
        "global_shift",
        float,
        {
            "argstr": "--tglobal",
            "help_string": "shift in fraction of TR, range 0:1 (default is 0.5 = no shift)",
        },
    ),
    (
        "custom_order",
        specs.File,
        {
            "argstr": "--ocustom={custom_order}",
            "help_string": "filename of single-column custom interleave order file (first slice is referred to as 1 not 0)",
        },
    ),
]
SliceTimer_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "slice_time_corrected_file",
        specs.File,
        {
            "help_string": "slice time corrected file",
            "requires": ["out_file"],
            "output_file_template": "{out_file}",
        },
    )
]
SliceTimer_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class SliceTimer(ShellCommandTask):
    input_spec = SliceTimer_input_spec
    output_spec = SliceTimer_output_spec
    executable = "slicetimer"
