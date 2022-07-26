import re, os, shutil, pytest
from pathlib import Path
from ..extractroi import ExtractROI


@pytest.mark.parametrize(
    "inputs, outputs",
    [({"in_file": "test.nii.gz", "t_min": 0, "t_size": 1}, ["roi_file"])],
)
def test_ExtractROI(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = ExtractROI(in_file=in_file)
    else:
        for key, val in inputs.items():
            try:
                pattern = r"\.[a-zA-Z]*"
                if isinstance(val, str):
                    if re.findall(pattern, val) != []:
                        inputs[key] = Path(test_data) / val
                    elif "_dir" in key:
                        dirpath = Path(test_data) / val
                        if dirpath.exists() and dirpath.is_dir():
                            shutil.rmtree(dirpath)
                        inputs[key] = Path(test_data) / val
                    else:
                        inputs[key] = eval(val)
                elif isinstance(val, list):
                    if all(re.findall(pattern, _) != [] for _ in val):
                        inputs[key] = [Path(test_data) / _ for _ in val]
                else:
                    inputs[key] = eval(val)
            except:
                pass
        task = ExtractROI(**inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
