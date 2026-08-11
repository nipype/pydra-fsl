from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.warp_utils import WarpUtils
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warputils_1():
    task = WarpUtils()
    task.in_file = Nifti1.sample(seed=0)
    task.reference = File.sample(seed=1)
    task.write_jacobian = False
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warputils_2():
    task = WarpUtils()
    task.in_file = Nifti1.sample(seed=0)
    task.out_format = "spline"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
