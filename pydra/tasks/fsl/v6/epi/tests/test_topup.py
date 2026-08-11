from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.topup import TOPUP
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_topup_1():
    task = TOPUP()
    task.in_file = Nifti1.sample(seed=0)
    task.encoding_file = File.sample(seed=1)
    task.out_warp_prefix = "warpfield"
    task.out_mat_prefix = "xfm"
    task.out_jac_prefix = "jac"
    task.config = "b02b0.cnf"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_topup_2():
    task = TOPUP()
    task.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
