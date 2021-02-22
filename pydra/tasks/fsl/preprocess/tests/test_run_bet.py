import os, pytest
from pathlib import Path
from ..bet import BET


@pytest.mark.xfail(
    "FSLDIR" not in os.environ, reason="no FSL found", raises=FileNotFoundError
)
@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (None, ["out_file"]),
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
def test_BET(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = BET(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
