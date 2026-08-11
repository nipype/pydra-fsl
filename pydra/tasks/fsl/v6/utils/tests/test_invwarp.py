from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.inv_warp import InvWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_invwarp_1():
    task = InvWarp()
    task.warp = Nifti1.sample(seed=0)
    task.reference = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_invwarp_2():
    task = InvWarp()
    task.warp = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
