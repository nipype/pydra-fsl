from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.first import FIRST
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_first_1():
    task = FIRST()
    task.in_file = File.sample(seed=0)
    task.out_file = "segmented"
    task.method = "auto"
    task.affine_file = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
