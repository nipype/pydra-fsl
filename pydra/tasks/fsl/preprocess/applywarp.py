from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "image to be warped",
            "argstr": "--in={in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "output filename",
            "argstr": "--out={out_file}",
            "position": 2,
            "output_file_template": "{in_file}_warp",
        },
    ),
    (
        "ref_file",
        specs.File,
        {
            "help_string": "reference image",
            "argstr": "--ref={ref_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "field_file",
        specs.File,
        {"help_string": "file containing warp field", "argstr": "--warp={field_file}"},
    ),
    (
        "abswarp",
        bool,
        {
            "help_string": "treat warp field as absolute: x' = w(x)",
            "argstr": "--abs",
            "xor": ["relwarp"],
        },
    ),
    (
        "relwarp",
        bool,
        {
            "help_string": "treat warp field as relative: x' = x + w(x)",
            "argstr": "--rel",
            "position": -1,
            "xor": ["abswarp"],
        },
    ),
    (
        "datatype",
        ty.Any,
        {
            "help_string": "Force output data type [char short int float double].",
            "argstr": "--datatype={datatype}",
        },
    ),
    (
        "supersample",
        bool,
        {
            "help_string": "intermediary supersampling of output, default is off",
            "argstr": "--super",
        },
    ),
    (
        "superlevel",
        ty.Any,
        {
            "help_string": "level of intermediary supersampling, a for 'automatic' or integer level. Default = 2",
            "argstr": "--superlevel={superlevel}",
        },
    ),
    (
        "premat",
        specs.File,
        {
            "help_string": "filename for pre-transform (affine matrix)",
            "argstr": "--premat={premat}",
        },
    ),
    (
        "postmat",
        specs.File,
        {
            "help_string": "filename for post-transform (affine matrix)",
            "argstr": "--postmat={postmat}",
        },
    ),
    (
        "mask_file",
        specs.File,
        {
            "help_string": "filename for mask image (in reference space)",
            "argstr": "--mask={mask_file}",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "help_string": "interpolation method",
            "argstr": "--interp={interp}",
            "position": -2,
        },
    ),
]
ApplyWarp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ApplyWarp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ApplyWarp(ShellCommandTask):
    input_spec = ApplyWarp_input_spec
    output_spec = ApplyWarp_output_spec
    executable = "applywarp"
