from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.threshold import Threshold
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_threshold_1():
    task = Threshold()
    task.direction = "below"
    task.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
