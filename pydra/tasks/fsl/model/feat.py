from pydra.engine import specs
from pydra import ShellCommandTask
import typing as ty


def FEAT_output(fsf_file):
    is_ica = False
    with open(fsf_file, "rt") as fp:
        text = fp.read()
        if "set fmri(inmelodic) 1" in text:
            is_ica = True
        for line in text.split("\n"):
            if line.find("set fmri(outputdir)") > -1:
                try:
                    outputdir_spec = line.split('"')[-2]
                    if os.path.exists(outputdir_spec):
                        outputs = outputdir_spec
                except:
                    pass

    if not outputs:
        if is_ica:
            outputs = glob(os.path.join(os.getcwd(), "*ica"))[0]
        else:
            outputs = glob(os.path.join(os.getcwd(), "*feat"))[0]
    print("Outputs from FEATmodel:", outputs)
    return outputs


input_fields = [
    (
        "fsf_file",
        specs.File,
        {
            "help_string": "File specifying the feat design spec file",
            "argstr": "{fsf_file}",
            "mandatory": True,
            "position": 0,
        },
    )
]
FEAT_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)

output_fields = [
    ("feat_dir", specs.Directory, {"requires": ["fsf_file"], "callable": FEAT_output})
]
FEAT_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class FEAT(ShellCommandTask):
    """
    Example
    -------
    >>> task = FEAT()
    >>> task.inputs.fsf_file = "test.fsf"
    >>> task.cmdline
    'feat test.fsf'
    """

    input_spec = FEAT_input_spec
    output_spec = FEAT_output_spec
    executable = "feat"