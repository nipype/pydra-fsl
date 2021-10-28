import pytest
import pydra
import os, imp
from pathlib import Path

from ..converter import FSLConverter

# TODO: rethink teh tests


@pytest.mark.skip()
def test_spec(tmpdir):
    interface_name = "BET"
    converter = FSLConverter(interface_name=interface_name)
    input_spec_pydra, output_spec_pydra = converter.pydra_specs()

    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"
    out_file = Path(os.path.dirname(__file__)) / "data_tests/test_brain.nii.gz"
    cmd = "bet"

    shelly = pydra.ShellCommandTask(
        name="bet_task",
        executable=cmd,
        input_spec=input_spec_pydra,
        output_spec=output_spec_pydra,
    )
    shelly.inputs.in_file = in_file
    assert shelly.inputs.executable == "bet"
    assert (
        shelly.cmdline
        == f"bet {in_file} {str(shelly.output_dir / 'test_brain.nii.gz')}"
    )
    res = shelly()
    assert res.output.out_file.exists()
    print("\n Result: ", res)

    shelly_mask = pydra.ShellCommandTask(
        name="bet_task",
        executable=cmd,
        input_spec=input_spec_pydra,
        output_spec=output_spec_pydra,
    )
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert (
        shelly_mask.cmdline
        == f"bet {in_file} {str(shelly_mask.output_dir / 'test_brain.nii.gz')} -m"
    )
    res = shelly_mask()
    assert res.output.out_file.exists()
    assert res.output.mask_file.exists()
    print("\n Result: ", res)


@pytest.mark.skip()
def test_spec_from_file(tmpdir):
    interface_name = "BET"
    converter = FSLConverter(interface_name=interface_name)

    dirname_spec = Path(tmpdir)
    (dirname_spec / "tests").mkdir()

    _, _ = converter.pydra_specs(write=True, dirname=dirname_spec)

    imp.load_source("bet_module", str(dirname_spec / "bet.py"))
    import bet_module as bm

    in_file = Path(os.path.dirname(__file__)) / "data_tests/test.nii.gz"

    shelly = bm.BET(name="my_bet")
    shelly.inputs.in_file = in_file
    assert shelly.inputs.executable == "bet"
    assert (
        shelly.cmdline
        == f"bet {in_file} {str(shelly.output_dir / 'test_brain.nii.gz')}"
    )
    res = shelly()
    assert res.output.out_file.exists()
    print("\n Result: ", res)

    shelly_mask = bm.BET(name="my_bet")
    shelly_mask.inputs.in_file = in_file
    shelly_mask.inputs.mask = True
    assert (
        shelly_mask.cmdline
        == f"bet {in_file} {str(shelly_mask.output_dir / 'test_brain.nii.gz')} -m"
    )
    res = shelly_mask()
    assert res.output.out_file.exists()
    assert res.output.mask_file.exists()
    print("\n Result: ", res)

    shelly_surf = bm.BET(name="my_bet")
    shelly_surf.inputs.in_file = in_file
    shelly_surf.inputs.surfaces = True
    assert (
        shelly_surf.cmdline
        == f"bet {in_file} {str(shelly_surf.output_dir / 'test_brain.nii.gz')} -A"
    )
    res = shelly_surf()
    assert res.output.out_file.exists()
    assert res.output.inskull_mask_file.exists()
    assert res.output.skull_mask_file.exists()
    print("\n Result: ", res)
