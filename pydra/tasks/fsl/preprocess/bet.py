from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file to skull strip",
            "argstr": "{in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "name of output skull stripped image",
            "argstr": "{out_file}",
            "position": 1,
            "output_file_template": "{in_file}_brain",
        },
    ),
    ("outline", bool, {"help_string": "create surface outline image", "argstr": "-o"}),
    ("mask", bool, {"help_string": "create binary mask image", "argstr": "-m"}),
    ("skull", bool, {"help_string": "create skull image", "argstr": "-s"}),
    (
        "no_output",
        bool,
        {"help_string": "Don't generate segmented output", "argstr": "-n"},
    ),
    (
        "frac",
        float,
        {"help_string": "fractional intensity threshold", "argstr": "-f {frac:.2f}"},
    ),
    (
        "vertical_gradient",
        float,
        {
            "help_string": "vertical gradient in fractional intensity threshold (-1, 1)",
            "argstr": "-g {vertical_gradient:.2f}",
        },
    ),
    ("radius", int, {"help_string": "head radius", "argstr": "-r {radius}"}),
    (
        "center",
        list,
        {"help_string": "center of gravity in voxels", "argstr": "-c {center}"},
    ),
    (
        "threshold",
        bool,
        {
            "help_string": "apply thresholding to segmented brain image and mask",
            "argstr": "-t",
        },
    ),
    (
        "mesh",
        bool,
        {"help_string": "generate a vtk mesh brain surface", "argstr": "-e"},
    ),
    (
        "robust",
        bool,
        {
            "help_string": "robust brain centre estimation (iterates BET several times)",
            "argstr": "-R",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "padding",
        bool,
        {
            "help_string": "improve BET if FOV is very small in Z (by temporarily padding end slices)",
            "argstr": "-Z",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "remove_eyes",
        bool,
        {
            "help_string": "eye & optic nerve cleanup (can be useful in SIENA)",
            "argstr": "-S",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "surfaces",
        bool,
        {
            "help_string": "run bet2 and then betsurf to get additional skull and scalp surfaces (includes registrations)",
            "argstr": "-A",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "t2_guided",
        str,
        {
            "help_string": "as with creating surfaces, when also feeding in non-brain-extracted T2 (includes registrations)",
            "argstr": "-A2 {t2_guided}",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "functional",
        bool,
        {
            "help_string": "apply to 4D fMRI data",
            "argstr": "-F",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
    (
        "reduce_bias",
        bool,
        {
            "help_string": "bias field and neck cleanup",
            "argstr": "-B",
            "xor": (
                "functional",
                "reduce_bias",
                "robust",
                "padding",
                "remove_eyes",
                "surfaces",
                "t2_guided",
            ),
        },
    ),
]
BET_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    (
        "mask_file",
        specs.File,
        {
            "help_string": "path/name of binary brain mask (if generated)",
            "requires": [[("mask", True)], [("reduce_bias", True)]],
            "output_file_template": "{out_file}_mask",
        },
    ),
    (
        "outline_file",
        specs.File,
        {
            "help_string": "path/name of outline file (if generated)",
            "requires": [("outline", True)],
            "output_file_template": "{out_file}_overlay",
        },
    ),
    (
        "meshfile",
        specs.File,
        {
            "help_string": "path/name of vtk mesh file (if generated)",
            "requires": [[("mesh", True)], [("surfaces", True)]],
            "output_file_template": "{out_file}_mesh.vtk",
        },
    ),
    (
        "inskull_mask_file",
        specs.File,
        {
            "help_string": "path/name of inskull mask (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_inskull_mask",
        },
    ),
    (
        "inskull_mesh_file",
        specs.File,
        {
            "help_string": "path/name of inskull mesh outline (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_inskull_mesh",
        },
    ),
    (
        "outskull_mask_file",
        specs.File,
        {
            "help_string": "path/name of outskull mask (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_outskull_mask",
        },
    ),
    (
        "outskull_mesh_file",
        specs.File,
        {
            "help_string": "path/name of outskull mesh outline (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_outskull_mesh",
        },
    ),
    (
        "outskin_mask_file",
        specs.File,
        {
            "help_string": "path/name of outskin mask (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_outskin_mask",
        },
    ),
    (
        "outskin_mesh_file",
        specs.File,
        {
            "help_string": "path/name of outskin mesh outline (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_outskin_mesh",
        },
    ),
    (
        "skull_mask_file",
        specs.File,
        {
            "help_string": "path/name of skull mask (if generated)",
            "requires": [("surfaces", True)],
            "output_file_template": "{out_file}_skull_mask",
        },
    ),
    (
        "skull_file",
        specs.File,
        {
            "help_string": "path/name of skull file (if generated)",
            "requires": [("skull", True)],
            "output_file_template": "{out_file}_skull",
        },
    ),
]
BET_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class BET(ShellCommandTask):
    """
    Example
    -------
    >>> task = BET()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.out_file = "test_brain.nii.gz"
    >>> task.inputs.frac = 0.7
    >>> task.cmdline
    'bet test.nii.gz test_brain.nii.gz -f 0.70'
    """

    input_spec = BET_input_spec
    output_spec = BET_output_spec
    executable = "bet"
