import os, pytest
from pathlib import Path
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
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = BET(in_file=in_file, **inputs)
    res = task()
    print("RESULT: ", res)
    if isinstance(outputs, str):
        outputs = [outputs]
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
