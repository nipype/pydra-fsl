from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.motion_outliers import MotionOutliers
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_motionoutliers_1():
    task = MotionOutliers()
    task.in_file = Nifti1.sample(seed=0)
    task.mask = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_motionoutliers_2():
    task = MotionOutliers()
    task.in_file = Nifti1.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
