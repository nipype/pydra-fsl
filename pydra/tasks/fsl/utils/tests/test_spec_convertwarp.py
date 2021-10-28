import os, pytest
from pathlib import Path
from ..convertwarp import ConvertWarp


@pytest.mark.parametrize("inputs, outputs", [])
def test_ConvertWarp(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ConvertWarp(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_ConvertWarp_exception(test_data, inputs, error):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ConvertWarp(in_file=in_file, **inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
