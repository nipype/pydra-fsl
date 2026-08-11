from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.sig_loss import SigLoss
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_sigloss_1():
    task = SigLoss()
    task.in_file = File.sample(seed=0)
    task.mask_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
