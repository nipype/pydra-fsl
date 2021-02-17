import os, pytest
from pathlib import Path
from ..fnirt import FNIRT


@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (
            {"ref_file": 'f"{in_file}"'},
            [
                "warped_file",
                "field_file",
                "jacobian_file",
                "modulatedref_file",
                "log_file",
                "fieldcoeff_file",
            ],
        )
    ],
)
def test_FNIRT(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = FNIRT(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_FNIRT_exception(test_data, inputs, error):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = FNIRT(in_file=in_file, **inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
