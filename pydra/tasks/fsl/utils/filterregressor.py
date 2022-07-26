from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file name (4D image)",
            "argstr": "-i {in_file}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "output file name for the filtered data",
            "argstr": "-o {out_file}",
            "position": 2,
            "output_file_template": "{in_file}_filtered",
        },
    ),
    (
        "design_file",
        specs.File,
        {
            "help_string": "name of the matrix with time courses (e.g. GLM design or MELODIC mixing matrix)",
            "argstr": "-d {design_file}",
            "mandatory": True,
            "position": 3,
        },
    ),
    (
        "filter_columns",
        list,
        {
            "help_string": "(1-based) column indices to filter out of the data",
            "argstr": "-f '{filter_columns}'",
            "mandatory": True,
            "position": 4,
            "xor": ["filter_all"],
        },
    ),
    (
        "mask",
        specs.File,
        {"help_string": "mask image file name", "argstr": "-m {mask}"},
    ),
    (
        "var_norm",
        bool,
        {"help_string": "perform variance-normalization on data", "argstr": "--vn"},
    ),
    (
        "out_vnscales",
        bool,
        {
            "help_string": "output scaling factors for variance normalization",
            "argstr": "--out_vnscales",
        },
    ),
]
FilterRegressor_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = []
FilterRegressor_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FilterRegressor(ShellCommandTask):
    """
    Example
    -------
    >>> task = FilterRegressor()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.design_file = "design"
    >>> task.inputs.filter_columns = "1,2,3"
    >>> task.inputs.out_file = "test_filtered.nii.gz"
    >>> task.cmdline
    'fsl_regfilt -i test.nii.gz -o test_filtered.nii.gz -d design -f 1,2,3'
    """

    input_spec = FilterRegressor_input_spec
    output_spec = FilterRegressor_output_spec
    executable = "fsl_regfilt"
