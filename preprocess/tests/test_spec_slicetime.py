import os, pytest
from pathlib import Path
from ..slicetime import SliceTimer


@pytest.mark.parametrize(
    "inputs, outputs",
    [({"ref_file": 'f"{in_file}"'}, ["out_file", "slice_time_corrected_file"])],
)
def test_SliceTimer(inputs, outputs):
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = SliceTimer(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
