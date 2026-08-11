from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.fix.cleaner import Cleaner
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cleaner_1():
    task = Cleaner()
    task.artifacts_list_file = File.sample(seed=0)
    task.highpass = 100
    task.confound_file = File.sample(seed=4)
    task.confound_file_1 = File.sample(seed=5)
    task.confound_file_2 = File.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
