from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.smm import SMM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smm_1():
    task = SMM()
    task.spatial_data_file = File.sample(seed=0)
    task.mask = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
