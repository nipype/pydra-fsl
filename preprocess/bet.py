from pydra.engine import specs
import traits
import attr

input_fields = [
    (
        "in_file",
        "File",
        {
            "argstr": "{in_file}",
            "help_string": "input file to skull strip",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        "str",
        {
            "argstr": "{out_file}",
            "help_string": "name of output skull stripped image",
            "position": 2,
            "output_file_template": "{in_file}_brain",
        },
    ),
    (
        "outline",
        "bool",
        {"argstr": "-o", "help_string": "create surface outline image"},
    ),
    ("mask", "bool", {"argstr": "-m", "help_string": "create binary mask image"}),
    ("skull", "bool", {"argstr": "-s", "help_string": "create skull image"}),
    (
        "no_output",
        "bool",
        {"argstr": "-n", "help_string": "Don't generate segmented output"},
    ),
    (
        "frac",
        "float",
        {"argstr": "-f {frac}", "help_string": "fractional intensity threshold"},
    ),
    (
        "vertical_gradient",
        "float",
        {
            "argstr": "-g {vertical_gradient}",
            "help_string": "vertical gradient in fractional intensity threshold (-1, 1)",
        },
    ),
    ("radius", "int", {"argstr": "-r {radius}", "help_string": "head radius"}),
    (
        "center",
        "list",
        {"argstr": "-c {center}", "help_string": "center of gravity in voxels"},
    ),
    (
        "threshold",
        "bool",
        {
            "argstr": "-t",
            "help_string": "apply thresholding to segmented brain image and mask",
        },
    ),
    (
        "mesh",
        "bool",
        {"argstr": "-e", "help_string": "generate a vtk mesh brain surface"},
    ),
    (
        "robust",
        "bool",
        {
            "argstr": "-R",
            "help_string": "robust brain centre estimation (iterates BET several times)",
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
        "bool",
        {
            "argstr": "-Z",
            "help_string": "improve BET if FOV is very small in Z (by temporarily padding end slices)",
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
        "bool",
        {
            "argstr": "-S",
            "help_string": "eye & optic nerve cleanup (can be useful in SIENA)",
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
        "bool",
        {
            "argstr": "-A",
            "help_string": "run bet2 and then betsurf to get additional skull and scalp surfaces (includes registrations)",
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
        "File",
        {
            "argstr": "-A2 {t2_guided}",
            "help_string": "as with creating surfaces, when also feeding in non-brain-extracted T2 (includes registrations)",
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
        "bool",
        {
            "argstr": "-F",
            "help_string": "apply to 4D fMRI data",
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
        "bool",
        {
            "argstr": "-B",
            "help_string": "bias field and neck cleanup",
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
input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=specs.ShellSpec)

output_fields = [
    (
        "out_file",
        "File",
        {
            "help_string": "path/name of skullstripped file (if generated)",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_brain",
        },
    ),
    (
        "mask_file",
        "File",
        {
            "help_string": "path/name of binary brain mask (if generated)",
            "requires": ["in_file", "mask"],
            "output_file_template": "{out_file}_mask",
        },
    ),
    (
        "outline_file",
        "File",
        {
            "help_string": "path/name of outline file (if generated)",
            "requires": ["in_file", "outline"],
            "output_file_template": "{out_file}_overlay",
        },
    ),
    (
        "meshfile",
        "File",
        {
            "help_string": "path/name of vtk mesh file (if generated)",
            "requires": ["in_file", "mesh"],
            "output_file_template": "{out_file}_mesh.vtk",
        },
    ),
    (
        "inskull_mask_file",
        "File",
        {
            "help_string": "path/name of inskull mask (if generated)",
            "requires": ["in_file", "mask", "skull"],
            "output_file_template": "{out_file}_inskull_mask",
        },
    ),
    (
        "inskull_mesh_file",
        "File",
        {
            "help_string": "path/name of inskull mesh outline (if generated)",
            "requires": ["in_file", "mesh", "skull"],
            "output_file_template": "{out_file}_inskull_mesh",
        },
    ),
    (
        "outskull_mask_file",
        "File",
        {
            "help_string": "path/name of outskull mask (if generated)",
            "requires": ["in_file", "mask", "skull"],
            "output_file_template": "{out_file}_outskull_mask",
        },
    ),
    (
        "outskull_mesh_file",
        "File",
        {
            "help_string": "path/name of outskull mesh outline (if generated)",
            "requires": ["in_file", "mesh", "skull"],
            "output_file_template": "{out_file}_outskull_mesh",
        },
    ),
]
output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=specs.ShellOutSpec
)

cmd = "bet"
