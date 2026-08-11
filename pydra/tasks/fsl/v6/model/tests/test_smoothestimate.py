from fileformats.generic import File
from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.smooth_estimate import SmoothEstimate
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_smoothestimate_1():
    task = SmoothEstimate()
    task.mask_file = File.sample(seed=1)
    task.residual_fit_file = File.sample(seed=2)
    task.zstat_file = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_smoothestimate_2():
    task = SmoothEstimate()
    task.zstat_file = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
