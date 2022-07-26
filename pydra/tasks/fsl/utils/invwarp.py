from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "warp",
        specs.File,
        {
            "help_string": "Name of file containing warp-coefficients/fields. This would typically be the output from the --cout switch of fnirt (but can also use fields, like the output from --fout).",
            "argstr": "--warp={warp}",
            "mandatory": True,
        },
    ),
    (
        "reference",
        specs.File,
        {
            "help_string": "Name of a file in target space. Note that the target space is now different from the target space that was used to create the --warp file. It would typically be the file that was specified with the --in argument when running fnirt.",
            "argstr": "--ref={reference}",
            "mandatory": True,
        },
    ),
    (
        "inverse_warp",
        str,
        {
            "help_string": 'Name of output file, containing warps that are the "reverse" of those in --warp. This will be a field-file (rather than a file of spline coefficients), and it will have any affine component included as part of the displacements.',
            "argstr": "--out={inverse_warp}",
            "output_file_template": "{warp}_inverse",
        },
    ),
    (
        "absolute",
        bool,
        {
            "help_string": "If set it indicates that the warps in --warp should be interpreted as absolute, provided that it is not created by fnirt (which always uses relative warps). If set it also indicates that the output --out should be absolute.",
            "argstr": "--abs",
            "xor": ["relative"],
        },
    ),
    (
        "relative",
        bool,
        {
            "help_string": "If set it indicates that the warps in --warp should be interpreted as relative. I.e. the values in --warp are displacements from the coordinates in the --ref space. If set it also indicates that the output --out should be relative.",
            "argstr": "--rel",
            "xor": ["absolute"],
        },
    ),
    (
        "niter",
        int,
        {
            "help_string": "Determines how many iterations of the gradient-descent search that should be run.",
            "argstr": "--niter={niter}",
        },
    ),
    (
        "regularise",
        float,
        {
            "help_string": "Regularization strength (deafult=1.0).",
            "argstr": "--regularise={regularise}",
        },
    ),
    (
        "noconstraint",
        bool,
        {"help_string": "Do not apply Jacobian constraint", "argstr": "--noconstraint"},
    ),
    (
        "jacobian_min",
        float,
        {
            "help_string": "Minimum acceptable Jacobian value for constraint (default 0.01)",
            "argstr": "--jmin={jacobian_min}",
        },
    ),
    (
        "jacobian_max",
        float,
        {
            "help_string": "Maximum acceptable Jacobian value for constraint (default 100.0)",
            "argstr": "--jmax={jacobian_max}",
        },
    ),
]
InvWarp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
InvWarp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class InvWarp(ShellCommandTask):
    """
    Example
    -------
    >>> task = InvWarp()
    >>> task.inputs.reference = "anatomical.nii"
    >>> task.inputs.warp = "struct2mni.nii"
    >>> task.inputs.inverse_warp = "struct2mni_inverse.nii.gz"
    >>> task.cmdline
    'invwarp --warp=struct2mni.nii --ref=anatomical.nii --out=struct2mni_inverse.nii.gz'
    """

    input_spec = InvWarp_input_spec
    output_spec = InvWarp_output_spec
    executable = "invwarp"
