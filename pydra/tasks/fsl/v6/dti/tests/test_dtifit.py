from fileformats.generic import File
from fileformats.medimage import Bval, Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.dti_fit import DTIFit
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_dtifit_1():
    task = DTIFit()
    task.dwi = Nifti1.sample(seed=0)
    task.base_name = "dtifit_"
    task.mask = Nifti1.sample(seed=2)
    task.bvecs = File.sample(seed=3)
    task.bvals = Bval.sample(seed=4)
    task.cni = File.sample(seed=13)
    task.gradnonlin = File.sample(seed=15)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_dtifit_2():
    task = DTIFit()
    task.dwi = Nifti1.sample(seed=0)
    task.mask = Nifti1.sample(seed=2)
    task.bvals = Bval.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
