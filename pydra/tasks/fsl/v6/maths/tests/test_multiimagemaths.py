from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.multi_image_maths import MultiImageMaths
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_multiimagemaths_1():
    task = MultiImageMaths()
    task.operand_files = [Nifti1.sample(seed=1)]
    task.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_multiimagemaths_2():
    task = MultiImageMaths()
    task.operand_files = [Nifti1.sample(seed=1)]
    task.in_file = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
