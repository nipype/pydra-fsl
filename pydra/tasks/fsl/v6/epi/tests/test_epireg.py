from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.epi_reg import EpiReg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_epireg_1():
    task = EpiReg()
    task.epi = Nifti1.sample(seed=0)
    task.t1_head = File.sample(seed=1)
    task.t1_brain = Nifti1.sample(seed=2)
    task.out_base = "epi2struct"
    task.fmap = Nifti1.sample(seed=4)
    task.fmapmag = File.sample(seed=5)
    task.fmapmagbrain = Nifti1.sample(seed=6)
    task.wmseg = File.sample(seed=7)
    task.weight_image = File.sample(seed=10)
    task.no_clean = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_epireg_2():
    task = EpiReg()
    task.epi = Nifti1.sample(seed=0)
    task.t1_brain = Nifti1.sample(seed=2)
    task.fmap = Nifti1.sample(seed=4)
    task.fmapmagbrain = Nifti1.sample(seed=6)
    task.pedir = "y"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
