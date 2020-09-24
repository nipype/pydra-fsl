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
            [
                "out_file",
                "meshfile",
                "inskull_mask_file",
                "inskull_mesh_file",
                "outskull_mask_file",
                "outskull_mesh_file",
                "outskin_mask_file",
                "outskin_mesh_file",
                "skull_mask_file",
            ],
        ),
    ],
)
def test_BET(inputs, outputs):
    if inputs is None:
        inputs = {}
    if isinstance(outputs, str):
        outputs = [outputs]
    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    task = BET(in_file=in_file, **inputs)
    assert task.generated_output_names == ["return_code", "stdout", "stderr"] + outputs
