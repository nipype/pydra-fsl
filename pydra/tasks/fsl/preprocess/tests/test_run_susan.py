import os, pytest
from pathlib import Path
from ..susan import SUSAN


@pytest.mark.skipif("FSLDIR" not in os.environ, reason="no FSL found")
@pytest.mark.parametrize(
    "inputs, outputs",
    [({"brightness_threshold": 0.01, "fwhm": 2}, ["out_file", "smoothed_file"])],
)
def test_SUSAN(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = SUSAN(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_SUSAN_exception(test_data, inputs, error):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = SUSAN(in_file=in_file, **inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
