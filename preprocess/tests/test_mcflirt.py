import pytest
from ..mcflirt import MCFLIRT


@pytest.mark.parametrize("inputs, outputs", [(None, "out_file")])
def test_MCFLIRT(inputs, outputs):
    if inputs is None:
        inputs = {}
    task = MCFLIRT(
        in_file="/pydra_fsl/tools/../preprocess/tests/data_tests/test.nii.gz", **inputs
    )
    res = task()
    print("RESULT: ", res)
    if isinstance(outputs, str):
        outputs = [outputs]
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
