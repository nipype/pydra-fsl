from fileformats.generic import File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.apply_topup import ApplyTOPUP
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applytopup_1():
    task = ApplyTOPUP()
    task.in_files = [Nifti1.sample(seed=0)]
    task.encoding_file = File.sample(seed=1)
    task.in_topup_fieldcoef = NiftiGz.sample(seed=3)
    task.in_topup_movpar = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_applytopup_2():
    task = ApplyTOPUP()
    task.in_files = [Nifti1.sample(seed=0)]
    task.in_topup_fieldcoef = NiftiGz.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
