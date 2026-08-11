from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.feat import FEAT
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_feat_1():
    task = FEAT()
    task.fsf_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
