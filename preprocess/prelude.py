from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "complex_phase_file",
        specs.File,
        {
            "argstr": "--complex={complex_phase_file}",
            "help_string": "complex phase input volume",
            "mandatory": True,
            "xor": ["magnitude_file", "phase_file"],
        },
    ),
    (
        "magnitude_file",
        specs.File,
        {
            "argstr": "--abs={magnitude_file}",
            "help_string": "file containing magnitude image",
            "mandatory": True,
            "xor": ["complex_phase_file"],
        },
    ),
    (
        "phase_file",
        specs.File,
        {
            "argstr": "--phase={phase_file}",
            "help_string": "raw phase file",
            "mandatory": True,
            "xor": ["complex_phase_file"],
        },
    ),
    (
        "unwrapped_phase_file",
        str,
        {
            "argstr": "--unwrap={unwrapped_phase_file}",
            "help_string": "file containing unwrapepd phase",
            "output_file_template": "{phase_file}_unwrapped",
        },
    ),
    (
        "num_partitions",
        int,
        {
            "argstr": "--numphasesplit={num_partitions}",
            "help_string": "number of phase partitions to use",
        },
    ),
    (
        "labelprocess2d",
        bool,
        {
            "argstr": "--labelslices",
            "help_string": "does label processing in 2D (slice at a time)",
        },
    ),
    (
        "process2d",
        bool,
        {
            "argstr": "--slices",
            "help_string": "does all processing in 2D (slice at a time)",
            "xor": ["labelprocess2d"],
        },
    ),
    (
        "process3d",
        bool,
        {
            "argstr": "--force3D",
            "help_string": "forces all processing to be full 3D",
            "xor": ["labelprocess2d", "process2d"],
        },
    ),
    (
        "threshold",
        float,
        {
            "argstr": "--thresh={threshold:.10f}",
            "help_string": "intensity threshold for masking",
        },
    ),
    (
        "mask_file",
        specs.File,
        {
            "argstr": "--mask={mask_file}",
            "help_string": "filename of mask input volume",
        },
    ),
    (
        "start",
        int,
        {
            "argstr": "--start={start}",
            "help_string": "first image number to process (default 0)",
        },
    ),
    (
        "end",
        int,
        {
            "argstr": "--end={end}",
            "help_string": "final image number to process (default Inf)",
        },
    ),
    (
        "savemask_file",
        str,
        {
            "argstr": "--savemask={savemask_file}",
            "help_string": "saving the mask volume",
        },
    ),
    (
        "rawphase_file",
        str,
        {
            "argstr": "--rawphase={rawphase_file}",
            "help_string": "saving the raw phase output",
        },
    ),
    (
        "label_file",
        str,
        {
            "argstr": "--labels={label_file}",
            "help_string": "saving the area labels output",
        },
    ),
    (
        "removeramps",
        bool,
        {
            "argstr": "--removeramps",
            "help_string": "remove phase ramps during unwrapping",
        },
    ),
]
PRELUDE_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
PRELUDE_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PRELUDE(ShellCommandTask):
    input_spec = PRELUDE_input_spec
    output_spec = PRELUDE_output_spec
    executable = "prelude"
