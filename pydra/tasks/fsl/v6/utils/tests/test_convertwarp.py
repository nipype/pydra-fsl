from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.convert_warp import ConvertWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_convertwarp_1():
    task = ConvertWarp()
    task.reference = File.sample(seed=0)
    task.premat = File.sample(seed=2)
    task.warp1 = Nifti1.sample(seed=3)
    task.midmat = File.sample(seed=4)
    task.warp2 = File.sample(seed=5)
    task.postmat = File.sample(seed=6)
    task.shift_in_file = File.sample(seed=7)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_convertwarp_2():
    task = ConvertWarp()
    task.warp1 = Nifti1.sample(seed=3)
    task.relwarp = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
