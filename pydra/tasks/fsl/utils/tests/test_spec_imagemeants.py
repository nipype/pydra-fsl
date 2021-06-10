import os, pytest
from pathlib import Path
from ..imagemeants import ImageMeants


@pytest.mark.parametrize("inputs, outputs", [(None, ["out_file"])])
def test_ImageMeants(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ImageMeants(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
