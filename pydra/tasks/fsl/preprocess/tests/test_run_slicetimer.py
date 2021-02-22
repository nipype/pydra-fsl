import os, pytest
from pathlib import Path
from ..slicetimer import SliceTimer


@pytest.mark.skipif("FSLDIR" not in os.environ, reason="no FSL found")
@pytest.mark.parametrize(
    "inputs, outputs",
    [({"ref_file": 'f"{in_file}"'}, ["out_file", "slice_time_corrected_file"])],
)
def test_SliceTimer(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
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
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
