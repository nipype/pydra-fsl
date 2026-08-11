from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.x_fibres_5 import XFibres5
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_xfibres5_1():
    task = XFibres5()
    task.gradnonlin = File.sample(seed=0)
    task.dwi = File.sample(seed=1)
    task.mask = File.sample(seed=2)
    task.bvecs = File.sample(seed=3)
    task.bvals = File.sample(seed=4)
    task.logdir = Directory.sample(seed=5)
    task.n_fibres = 2
    task.n_jumps = 5000
    task.burn_in = 0
    task.burn_in_no_ard = 0
    task.sample_every = 1
    task.update_proposal_every = 40
    task.force_dir = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
