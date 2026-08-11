from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.contrast_mgr import ContrastMgr
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_contrastmgr_1():
    task = ContrastMgr()
    task.tcon_file = File.sample(seed=0)
    task.fcon_file = File.sample(seed=1)
    task.param_estimates = [File.sample(seed=2)]
    task.corrections = File.sample(seed=3)
    task.dof_file = File.sample(seed=4)
    task.sigmasquareds = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
