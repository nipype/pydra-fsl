from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "filename of input timeseries",
            "argstr": "--in={in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "filename of output timeseries",
            "argstr": "--out={out_file}",
            "output_file_template": "{in_file}_st",
        },
    ),
    (
        "index_dir",
        bool,
        {"help_string": "slice indexing from top to bottom", "argstr": "--down"},
    ),
    (
        "time_repetition",
        float,
        {
            "help_string": "Specify TR of data - default is 3s",
            "argstr": "--repeat={time_repetition}",
        },
    ),
    (
        "slice_direction",
        ty.Any,
        {
            "help_string": "direction of slice acquisition (x=1, y=2, z=3) - default is z",
            "argstr": "--direction={slice_direction}",
        },
    ),
    (
        "interleaved",
        bool,
        {"help_string": "use interleaved acquisition", "argstr": "--odd"},
    ),
    (
        "custom_timings",
        specs.File,
        {
            "help_string": "slice timings, in fractions of TR, range 0:1 (default is 0.5 = no shift)",
            "argstr": "--tcustom={custom_timings}",
        },
    ),
    (
        "global_shift",
        float,
        {
            "help_string": "shift in fraction of TR, range 0:1 (default is 0.5 = no shift)",
            "argstr": "--tglobal",
        },
    ),
    (
        "custom_order",
        specs.File,
        {
            "help_string": "filename of single-column custom interleave order file (first slice is referred to as 1 not 0)",
            "argstr": "--ocustom={custom_order}",
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
