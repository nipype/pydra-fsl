from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "reference",
        specs.File,
        {
            "help_string": "Name of a file in target space of the full transform.",
            "argstr": "--ref={reference}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "Name of output file, containing warps that are the combination of all those given as arguments. The format of this will be a field-file (rather than spline coefficients) with any affine components included.",
            "argstr": "--out={out_file}",
            "position": -1,
            "output_file_template": "{reference}_concatwarp",
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
        "warp1",
        specs.File,
        {
            "help_string": "Name of file containing initial warp-fields/coefficients (follows premat). This could e.g. be a fnirt-transform from a subjects structural scan to an average of a group of subjects.",
            "argstr": "--warp1={warp1}",
        },
    ),
    (
        "midmat",
        specs.File,
        {
            "help_string": "Name of file containing mid-warp-affine transform",
            "argstr": "--midmat={midmat}",
        },
    ),
    (
        "warp2",
        specs.File,
        {
            "help_string": "Name of file containing secondary warp-fields/coefficients (after warp1/midmat but before postmat). This could e.g. be a fnirt-transform from the average of a group of subjects to some standard space (e.g. MNI152).",
            "argstr": "--warp2={warp2}",
        },
    ),
    (
        "postmat",
        specs.File,
        {
            "help_string": "Name of file containing an affine transform (applied last). It could e.g. be an affine transform that maps the MNI152-space into a better approximation to the Talairach-space (if indeed there is one).",
            "argstr": "--postmat={postmat}",
        },
    ),
    (
        "shift_in_file",
        specs.File,
        {
            "help_string": 'Name of file containing a "shiftmap", a non-linear transform with displacements only in one direction (applied first, before premat). This would typically be a fieldmap that has been pre-processed using fugue that maps a subjects functional (EPI) data onto an undistorted space (i.e. a space that corresponds to his/her true anatomy).',
            "argstr": "--shiftmap={shift_in_file}",
        },
    ),
    (
        "shift_direction",
        ty.Any,
        {
            "help_string": "Indicates the direction that the distortions from --shiftmap goes. It depends on the direction and polarity of the phase-encoding in the EPI sequence.",
            "argstr": "--shiftdir={shift_direction}",
            "requires": ["shift_in_file"],
        },
    ),
    (
        "cons_jacobian",
        bool,
        {
            "help_string": "Constrain the Jacobian of the warpfield to lie within specified min/max limits.",
            "argstr": "--constrainj",
        },
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
    (
        "abswarp",
        bool,
        {
            "help_string": "If set it indicates that the warps in --warp1 and --warp2 should be interpreted as absolute. I.e. the values in --warp1/2 are the coordinates in the next space, rather than displacements. This flag is ignored if --warp1/2 was created by fnirt, which always creates relative displacements.",
            "argstr": "--abs",
            "xor": ["relwarp"],
        },
    ),
    (
        "relwarp",
        bool,
        {
            "help_string": "If set it indicates that the warps in --warp1/2 should be interpreted as relative. I.e. the values in --warp1/2 are displacements from the coordinates in the next space.",
            "argstr": "--rel",
            "xor": ["abswarp"],
        },
    ),
    (
        "out_abswarp",
        bool,
        {
            "help_string": "If set it indicates that the warps in --out should be absolute, i.e. the values in --out are displacements from the coordinates in --ref.",
            "argstr": "--absout",
            "xor": ["out_relwarp"],
        },
    ),
    (
        "out_relwarp",
        bool,
        {
            "help_string": "If set it indicates that the warps in --out should be relative, i.e. the values in --out are displacements from the coordinates in --ref.",
            "argstr": "--relout",
            "xor": ["out_abswarp"],
        },
    ),
]
ConvertWarp_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
ConvertWarp_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class ConvertWarp(ShellCommandTask):
    """
    Example
    -------
    >>> task = ConvertWarp()
    >>> task.inputs.warp1 = "warpfield.nii"
    >>> task.inputs.reference = "T1.nii"
    >>> task.inputs.relwarp = True
    >>> task.cmdline
    'convertwarp --ref=T1.nii --rel --warp1=warpfield.nii --out=T1_concatwarp.nii.gz'
    """

    input_spec = ConvertWarp_input_spec
    output_spec = ConvertWarp_output_spec
    executable = "convertwarp"
