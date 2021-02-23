from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "argstr": "--in={in_file}",
            "help_string": "image to be warped",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "argstr": "--out={out_file}",
            "help_string": "output filename",
            "position": 2,
            "output_file_template": "{in_file}_warp",
        },
    ),
    (
        "ref_file",
        specs.File,
        {
            "argstr": "--ref={ref_file}",
            "help_string": "reference image",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "field_file",
        specs.File,
        {"argstr": "--warp={field_file}", "help_string": "file containing warp field"},
    ),
    (
        "abswarp",
        bool,
        {
            "argstr": "--abs",
            "help_string": "treat warp field as absolute: x' = w(x)",
            "xor": ["relwarp"],
        },
    ),
    (
        "relwarp",
        bool,
        {
            "argstr": "--rel",
            "help_string": "treat warp field as relative: x' = x + w(x)",
            "position": -1,
            "xor": ["abswarp"],
        },
    ),
    (
        "datatype",
        ty.Any,
        {
            "argstr": "--datatype={datatype}",
            "help_string": "Force output data type [char short int float double].",
        },
    ),
    (
        "supersample",
        bool,
        {
            "argstr": "--super",
            "help_string": "intermediary supersampling of output, default is off",
        },
    ),
    (
        "superlevel",
        ty.Any,
        {
            "argstr": "--superlevel={superlevel}",
            "help_string": "level of intermediary supersampling, a for 'automatic' or integer level. Default = 2",
        },
    ),
    (
        "premat",
        specs.File,
        {
            "argstr": "--premat={premat}",
            "help_string": "filename for pre-transform (affine matrix)",
        },
    ),
    (
        "postmat",
        specs.File,
        {
            "argstr": "--postmat={postmat}",
            "help_string": "filename for post-transform (affine matrix)",
        },
    ),
    (
        "mask_file",
        specs.File,
        {
            "argstr": "--mask={mask_file}",
            "help_string": "filename for mask image (in reference space)",
        },
    ),
    (
        "interp",
        ty.Any,
        {
            "argstr": "--interp={interp}",
            "help_string": "interpolation method",
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
