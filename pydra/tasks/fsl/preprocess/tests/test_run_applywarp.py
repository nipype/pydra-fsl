import os, pytest
from pathlib import Path
from ..applywarp import ApplyWarp


@pytest.mark.parametrize(
    "inputs, outputs", [({"ref_file": 'f"{in_file}"'}, ["out_file"])]
)
def test_ApplyWarp(inputs, outputs):
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ApplyWarp(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
