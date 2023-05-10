import re, os, shutil, pytest
from pathlib import Path
from ..eddy import Eddy


@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (
            {
                "in_file": "test.nii.gz",
                "in_mask": "mask.nii.gz",
                "in_index": "test_index.txt",
                "in_acqp": "test_acqp.txt",
                "in_bvec": "bvecs.scheme",
                "in_bval": "bvals.scheme",
            },
            [
                "out_corrected",
                "out_parameter",
                "out_movement_rms",
                "out_restricted_movement_rms",
                "out_shell_alignment_parameters",
                "out_shell_pe_translation_parameters",
                "out_outlier_map",
                "out_outlier_n_stdev_map",
                "out_outlier_n_sqr_stdev_map",
                "out_outlier_report",
            ],
        )
    ],
)
def test_Eddy(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = Eddy(in_file=in_file)
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
        task = Eddy(**inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
