from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.susan import SUSAN
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_susan_1():
    task = SUSAN()
    task.in_file = File.sample(seed=0)
    task.dimension = 3
    task.use_median = 1
    task.usans = []
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
