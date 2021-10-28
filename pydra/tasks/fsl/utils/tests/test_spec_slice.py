import os, pytest
from pathlib import Path
from ..slice import Slice


@pytest.mark.parametrize("inputs, outputs", [(None, [])])
def test_Slice(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = Slice(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
