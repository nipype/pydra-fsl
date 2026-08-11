from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.apply_mask import ApplyMask
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applymask_1():
    task = ApplyMask()
    task.mask_file = File.sample(seed=0)
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
