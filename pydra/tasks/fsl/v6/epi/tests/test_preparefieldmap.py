from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.prepare_fieldmap import PrepareFieldmap
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_preparefieldmap_1():
    task = PrepareFieldmap()
    task.scanner = "SIEMENS"
    task.in_phase = Nifti1.sample(seed=1)
    task.in_magnitude = File.sample(seed=2)
    task.delta_TE = 2.46
    task.nocheck = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_preparefieldmap_2():
    task = PrepareFieldmap()
    task.in_phase = Nifti1.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
