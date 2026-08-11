from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.dual_regression import DualRegression
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dualregression_1():
    task = DualRegression()
    task.in_files = [Nifti1.sample(seed=0)]
    task.group_IC_maps_4D = File.sample(seed=1)
    task.des_norm = True
    task.design_file = File.sample(seed=4)
    task.con_file = File.sample(seed=5)
    task.out_dir = "output"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_dualregression_2():
    task = DualRegression()
    task.in_files = [Nifti1.sample(seed=0)]
    task.des_norm = False
    task.n_perm = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
