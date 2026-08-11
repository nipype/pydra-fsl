from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.bet import BET
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bet_1():
    task = BET()
    task.in_file = Nifti1.sample(seed=0)
    task.t2_guided = File.sample(seed=16)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bet_2():
    task = BET()
    task.in_file = Nifti1.sample(seed=0)
    task.out_file = "brain_anat.nii"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
