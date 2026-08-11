from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.epi_de_warp import EPIDeWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_epidewarp_1():
    task = EPIDeWarp()
    task.mag_file = File.sample(seed=0)
    task.dph_file = Nifti1.sample(seed=1)
    task.exf_file = File.sample(seed=2)
    task.epi_file = Nifti1.sample(seed=3)
    task.tediff = 2.46
    task.esp = 0.58
    task.sigma = 2
    task.nocleanup = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_epidewarp_2():
    task = EPIDeWarp()
    task.dph_file = Nifti1.sample(seed=1)
    task.epi_file = Nifti1.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
