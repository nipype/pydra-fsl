import os, pytest
from pathlib import Path
from ..flirt import FLIRT


@pytest.mark.parametrize("inputs, outputs", [])
def test_FLIRT(inputs, outputs):
    if inputs is None:
        inputs = {}
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = FLIRT(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_FLIRT_exception(inputs, error):
    if inputs is None:
        inputs = {}
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = FLIRT(in_file=in_file, **inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
