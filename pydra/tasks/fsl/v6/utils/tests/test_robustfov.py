from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.robust_fov import RobustFOV
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_robustfov_1():
    task = RobustFOV()
    task.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
