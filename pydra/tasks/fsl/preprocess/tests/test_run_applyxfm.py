import os, pytest
from pathlib import Path
from ..applyxfm import ApplyXFM


@pytest.mark.xfail("FSLDIR" not in os.environ, reason="no FSL found", raises=FileNotFoundError)
@pytest.mark.parametrize("inputs, outputs", [(None, ["out_file"])])
def test_ApplyXFM(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    reference = Path(test_data) / "test.nii.gz"
    in_matrix_file = Path(test_data) / "transform.mat"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ApplyXFM(in_file=in_file, reference=reference, in_matrix_file=in_matrix_file, **inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_ApplyXFM_exception(test_data, inputs, error):
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = ApplyXFM(**inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
