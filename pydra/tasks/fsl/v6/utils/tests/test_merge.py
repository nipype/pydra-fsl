from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.merge import Merge
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_merge_1():
    task = Merge()
    task.in_files = [Nifti1.sample(seed=0)]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_merge_2():
    task = Merge()
    task.in_files = [Nifti1.sample(seed=0)]
    task.tr = 2.25
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
