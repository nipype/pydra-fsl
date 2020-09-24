import os, pytest
from pathlib import Path
from ..mcflirt import MCFLIRT


@pytest.mark.parametrize("inputs, outputs", [(None, "out_file")])
def test_MCFLIRT(inputs, outputs):
    if inputs is None:
        inputs = {}
    if isinstance(outputs, str):
        outputs = [outputs]
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = MCFLIRT(in_file=in_file, **inputs)
    assert task.generated_output_names == ["return_code", "stdout", "stderr"] + outputs
