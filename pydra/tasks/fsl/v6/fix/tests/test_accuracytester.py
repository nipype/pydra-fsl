from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.fix.accuracy_tester import AccuracyTester
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_accuracytester_1():
    task = AccuracyTester()
    task.mel_icas = [Directory.sample(seed=0)]
    task.trained_wts_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
