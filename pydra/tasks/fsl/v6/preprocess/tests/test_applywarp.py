from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.apply_warp import ApplyWarp
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applywarp_1():
    task = ApplyWarp()
    task.in_file = File.sample(seed=0)
    task.ref_file = File.sample(seed=2)
    task.field_file = File.sample(seed=3)
    task.premat = File.sample(seed=9)
    task.postmat = File.sample(seed=10)
    task.mask_file = File.sample(seed=11)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
