from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.fugue import FUGUE
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fugue_1():
    task = FUGUE()
    task.in_file = Nifti1.sample(seed=0)
    task.shift_in_file = Nifti1.sample(seed=1)
    task.phasemap_in_file = Nifti1.sample(seed=2)
    task.fmap_in_file = File.sample(seed=3)
    task.forward_warping = False
    task.mask_file = Nifti1.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_2():
    task = FUGUE()
    task.in_file = Nifti1.sample(seed=0)
    task.shift_in_file = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_3():
    task = FUGUE()
    task.in_file = Nifti1.sample(seed=0)
    task.unwarp_direction = "y"
    task.mask_file = Nifti1.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fugue_4():
    task = FUGUE()
    task.phasemap_in_file = Nifti1.sample(seed=2)
    task.dwell_to_asym_ratio = (0.77e-3 * 3) / 2.46e-3
    task.save_shift = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
