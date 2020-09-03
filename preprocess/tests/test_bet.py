import pytest
from ..bet import BET


@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (None, "out_file"),
        ({"mask": True}, ["out_file", "mask_file"]),
        (
            {"surfaces": True},
            ["out_file", "inskull_mask_file", "inskull_mesh_file", "skull_mask_file"],
        ),
    ],
)
def test_BET(inputs, outputs):
    if inputs is None:
        inputs = {}
    task = BET(in_file="/pydra_fsl/tools/data_tests/test.nii.gz", **inputs)
    res = task()
    print("RESULT: ", res)
    if isinstance(outputs, str):
        outputs = [outputs]
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
