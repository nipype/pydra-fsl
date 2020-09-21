import os, pytest
from pathlib import Path
from ..mcflirt import MCFLIRT


@pytest.mark.parametrize("inputs, outputs", [(None, "out_file")])
def test_MCFLIRT(inputs, outputs):
    if inputs is None:
        inputs = {}
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = MCFLIRT(in_file=in_file, **inputs)
    res = task()
    print("RESULT: ", res)
    if isinstance(outputs, str):
        outputs = [outputs]
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
