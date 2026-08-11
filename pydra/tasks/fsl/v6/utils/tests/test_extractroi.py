from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.extract_roi import ExtractROI
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_extractroi_1():
    task = ExtractROI()
    task.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_extractroi_2():
    task = ExtractROI()
    task.in_file = File.sample(seed=0)
    task.roi_file = "bar.nii"
    task.t_min = 0
    task.t_size = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
