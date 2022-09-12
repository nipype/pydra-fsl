import re, os, shutil, pytest
from pathlib import Path
from ..featmodel import FEATModel


@pytest.mark.xfail("FSLDIR" not in os.environ, reason="no FSL found", raises=FileNotFoundError)
@pytest.mark.parametrize("inputs, outputs", [])
def test_FEATModel(test_data, inputs, outputs):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = FEATModel(in_file=in_file)
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
        task = FEATModel(**inputs)
    assert set(task.generated_output_names) == set(["return_code", "stdout", "stderr"] + outputs)
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        if isinstance(getattr(res.output, out_nm), list):
            assert [os.path.exists(x) for x in getattr(res.output, out_nm)]
        else:
            assert os.path.exists(getattr(res.output, out_nm))


@pytest.mark.parametrize("inputs, error", [(None, "AttributeError")])
def test_FEATModel_exception(test_data, inputs, error):
    if inputs is None:
        in_file = Path(test_data) / "test.nii.gz"
        task = FEATModel(in_file=in_file)
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
        task = FEATModel(**inputs)
    with pytest.raises(eval(error)):
        task.generated_output_names
