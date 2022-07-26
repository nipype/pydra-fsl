import re, os, shutil, pytest
from pathlib import Path
from ..flameo import FLAMEO


@pytest.mark.xfail("FSLDIR" not in os.environ, reason="no FSL found", raises=FileNotFoundError)
@pytest.mark.parametrize(
    "inputs, outputs",
    [
        (
            {
                "cope_file": "cope_merged.nii.gz",
                "var_cope_file": "varcope_merged.nii.gz",
                "cov_split_file": "design.grp",
                "design_file": "design.mat",
                "t_con_file": "design.con",
                "mask_file": "mask.nii.gz",
                "run_mode": "fe",
                "log_dir": "stats",
            },
            [
                "copes",
                "var_copes",
                "mrefvars",
                "pes",
                "res4d",
                "tdof",
                "weights",
                "tstats",
                "zstats",
                "stats_dir",
            ],
        )
    ],
)
def test_FLAMEO(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = FLAMEO(in_file=in_file)
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
        task = FLAMEO(**inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        if isinstance(getattr(res.output, out_nm), list):
            assert [os.path.exists(x) for x in getattr(res.output, out_nm)]
        else:
            assert os.path.exists(getattr(res.output, out_nm))
