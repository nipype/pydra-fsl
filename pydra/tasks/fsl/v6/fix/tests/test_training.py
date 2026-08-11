from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.fix.training import Training
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_training_1():
    task = Training()
    task.mel_icas = [Directory.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
