from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.possum.b0_calc import B0Calc
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_b0calc_1():
    task = B0Calc()
    task.in_file = Nifti1.sample(seed=0)
    task.x_grad = 0.0
    task.y_grad = 0.0
    task.z_grad = 0.0
    task.x_b0 = 0.0
    task.y_b0 = 0.0
    task.z_b0 = 1.0
    task.delta = -9.45e-06
    task.chi_air = 4e-07
    task.compute_xyz = False
    task.extendboundary = 1.0
    task.directconv = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_b0calc_2():
    task = B0Calc()
    task.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
