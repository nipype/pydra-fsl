from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.binary_maths import BinaryMaths
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_binarymaths_1():
    task = BinaryMaths()
    task.operand_file = File.sample(seed=1)
    task.in_file = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
