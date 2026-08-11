from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.eddy_correct import EddyCorrect
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_eddycorrect_1():
    task = EddyCorrect()
    task.in_file = Nifti1.sample(seed=0)
    task.ref_num = 0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddycorrect_2():
    task = EddyCorrect()
    task.in_file = Nifti1.sample(seed=0)
    task.out_file = "diffusion_edc.nii"
    task.ref_num = 0
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
