from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input data file",
            "argstr": "-i {in_file}",
            "copyfile": False,
            "mandatory": True,
            "position": -2,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "output data file",
            "argstr": "-o {out_file}",
            "mandatory": True,
            "position": -1,
        },
    ),
    (
        "verbose",
        bool,
        {"help_string": "Use verbose logging.", "argstr": "-v", "position": 1},
    ),
    (
        "brain_extracted",
        bool,
        {
            "help_string": "Input structural image is already brain-extracted",
            "argstr": "-b",
            "position": 2,
        },
    ),
    (
        "no_cleanup",
        bool,
        {
            "help_string": "Input structural image is already brain-extracted",
            "argstr": "-d",
            "position": 3,
        },
    ),
    (
        "method",
        ty.Any,
        "auto",
        {
            "help_string": "Method must be one of auto, fast, none, or it can be entered using the 'method_as_numerical_threshold' input",
            "argstr": "-m {method}",
            "position": 4,
            "xor": ["method_as_numerical_threshold"],
        },
    ),
    (
        "method_as_numerical_threshold",
        float,
        {
            "help_string": "Specify a numerical threshold value or use the 'method' input to choose auto, fast, or none",
            "argstr": "-m {method_as_numerical_threshold:.4f}",
            "position": 4,
        },
    ),
    (
        "list_of_specific_structures",
        list,
        {
            "help_string": "Runs only on the specified structures (e.g. L_Hipp, R_HippL_Accu, R_Accu, L_Amyg, R_AmygL_Caud, R_Caud, L_Pall, R_PallL_Puta, R_Puta, L_Thal, R_Thal, BrStem",
            "argstr": "-s {list_of_specific_structures}",
            "position": 5,
            "sep": ",",
        },
    ),
    (
        "affine_file",
        specs.File,
        {
            "help_string": "Affine matrix to use (e.g. img2std.mat) (does not re-run registration)",
            "argstr": "-a {affine_file}",
            "position": 6,
        },
    ),
]
FIRST_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))

output_fields = [
    (
        "vtk_surfaces",
        specs.MultiOutputFile,
        {
            "help_string": "VTK format meshes for each subcortical region",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_vtk_surfaces",
        },
    ),
    (
        "bvars",
        specs.MultiOutputFile,
        {
            "help_string": "bvars for each subcortical region",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_bvars",
        },
    ),
    (
        "original_segmentations",
        specs.File,
        {
            "help_string": "3D image file containing the segmented regions as integer values. Uses CMA labelling",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_original_segmentations",
        },
    ),
    (
        "segmentation_file",
        specs.File,
        {
            "help_string": "4D image file containing a single volume per segmented region",
            "requires": ["in_file"],
            "output_file_template": "{in_file}_segmentation_file",
        },
    ),
]
FIRST_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FIRST(ShellCommandTask):
    input_spec = FIRST_input_spec
    output_spec = FIRST_output_spec
    executable = "run_first_all"
