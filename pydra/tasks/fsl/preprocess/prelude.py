from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "complex_phase_file",
        specs.File,
        {
            "help_string": "complex phase input volume",
            "argstr": "--complex={complex_phase_file}",
            "mandatory": True,
            "xor": ["magnitude_file", "phase_file"],
        },
    ),
    (
        "magnitude_file",
        specs.File,
        {
            "help_string": "file containing magnitude image",
            "argstr": "--abs={magnitude_file}",
            "mandatory": True,
            "xor": ["complex_phase_file"],
        },
    ),
    (
        "phase_file",
        specs.File,
        {
            "help_string": "raw phase file",
            "argstr": "--phase={phase_file}",
            "mandatory": True,
            "xor": ["complex_phase_file"],
        },
    ),
    (
        "unwrapped_phase_file",
        str,
        {
            "help_string": "file containing unwrapepd phase",
            "argstr": "--unwrap={unwrapped_phase_file}",
            "output_file_template": "{phase_file}_unwrapped",
        },
    ),
    (
        "num_partitions",
        int,
        {
            "help_string": "number of phase partitions to use",
            "argstr": "--numphasesplit={num_partitions}",
        },
    ),
    (
        "labelprocess2d",
        bool,
        {
            "help_string": "does label processing in 2D (slice at a time)",
            "argstr": "--labelslices",
        },
    ),
    (
        "process2d",
        bool,
        {
            "help_string": "does all processing in 2D (slice at a time)",
            "argstr": "--slices",
            "xor": ["labelprocess2d"],
        },
    ),
    (
        "process3d",
        bool,
        {
            "help_string": "forces all processing to be full 3D",
            "argstr": "--force3D",
            "xor": ["labelprocess2d", "process2d"],
        },
    ),
    (
        "threshold",
        float,
        {
            "help_string": "intensity threshold for masking",
            "argstr": "--thresh={threshold:.10f}",
        },
    ),
    (
        "mask_file",
        specs.File,
        {
            "help_string": "filename of mask input volume",
            "argstr": "--mask={mask_file}",
        },
    ),
    (
        "start",
        int,
        {
            "help_string": "first image number to process (default 0)",
            "argstr": "--start={start}",
        },
    ),
    (
        "end",
        int,
        {
            "help_string": "final image number to process (default Inf)",
            "argstr": "--end={end}",
        },
    ),
    (
        "savemask_file",
        str,
        {
            "help_string": "saving the mask volume",
            "argstr": "--savemask={savemask_file}",
        },
    ),
    (
        "rawphase_file",
        str,
        {
            "help_string": "saving the raw phase output",
            "argstr": "--rawphase={rawphase_file}",
        },
    ),
    (
        "label_file",
        str,
        {
            "help_string": "saving the area labels output",
            "argstr": "--labels={label_file}",
        },
    ),
    (
        "removeramps",
        bool,
        {
            "help_string": "remove phase ramps during unwrapping",
            "argstr": "--removeramps",
        },
    ),
]
PRELUDE_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = []
PRELUDE_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class PRELUDE(ShellCommandTask):
    input_spec = PRELUDE_input_spec
    output_spec = PRELUDE_output_spec
    executable = "prelude"
