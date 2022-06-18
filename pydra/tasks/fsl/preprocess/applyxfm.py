from pydra.engine import specs
from pydra.tasks.fsl.preprocess.flirt import FLIRT

input_fields = [
    (
        "in_file",
        specs.File,
        {
            "help_string": "input file",
            "argstr": "-in {in_file}",
            "mandatory": True,
            "position": 0,
        },
    ),
    (
        "reference",
        specs.File,
        {
            "help_string": "reference file",
            "argstr": "-ref {reference}",
            "mandatory": True,
            "position": 1,
        },
    ),
    (
        "apply_xfm",
        bool,
        True,
        {
            "help_string": "apply transformation supplied by in_matrix_file or uses_qform to use the affine matrix stored in the reference header",
            "argstr": "-applyxfm",
        },
    ),
    (
        "in_matrix_file",
        str,
        {
            "help_string": "input 4x4 affine matrix",
            "argstr": "-init {in_matrix_file}",
            "mandatory": True,
        },
    ),
    (
        "out_file",
        str,
        {
            "help_string": "registered output file",
            "argstr": "-out {out_file}",
            "position": 2,
            "output_file_template": "{in_file}_flirt",
        },
    ),
]

ApplyXFM_input_spec = specs.SpecInfo(name="Input", fields=input_fields, bases=(specs.ShellSpec,))


class ApplyXFM(FLIRT):
    """
    Example
    -------
    >>> task = ApplyXFM()
    >>> task.inputs.in_file = 'test.nii.gz'
    >>> task.inputs.in_matrix_file = 'transform.mat'
    >>> task.inputs.reference = 'dest.nii.gz'
    >>> task.cmdline # doctest: +ELLIPSIS
    'flirt -in test.nii.gz -ref dest.nii.gz -out .../test_flirt.nii.gz -applyxfm -init transform.mat'

    # using a custom outfile
    >>> task.inputs.out_file = 'custom_outfile.nii.gz'
    >>> task.cmdline
    'flirt -in test.nii.gz -ref dest.nii.gz -out custom_outfile.nii.gz -applyxfm -init transform.mat'
    """

    input_spec = ApplyXFM_input_spec
