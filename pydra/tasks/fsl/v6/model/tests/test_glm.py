from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.glm import GLM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_glm_1():
    task = GLM()
    task.in_file = Nifti1.sample(seed=0)
    task.design = Nifti1.sample(seed=2)
    task.contrasts = File.sample(seed=3)
    task.mask = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_glm_2():
    task = GLM()
    task.in_file = Nifti1.sample(seed=0)
    task.design = Nifti1.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
