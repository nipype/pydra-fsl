from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.reorient_2_std import Reorient2Std
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_reorient2std_1():
    task = Reorient2Std()
    task.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
