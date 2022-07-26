import re, os, shutil, pytest
from pathlib import Path
from ..cluster import Cluster


@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (
            {"in_file": "zstat1.nii.gz", "threshold": 2.3, "use_mm": True},
            [
                "out_index_file",
                "out_localmax_txt_file",
                "out_localmax_vol_file",
                "out_threshold_file",
                "out_max_file",
                "out_mean_file",
                "out_pval_file",
                "out_size_file",
                "out_threshold_file",
            ],
        )
    ],
)
def test_Cluster(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = Cluster(in_file=in_file)
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
        task = Cluster(**inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
