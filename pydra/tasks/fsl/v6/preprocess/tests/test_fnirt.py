from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.fnirt import FNIRT
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_fnirt_1():
    task = FNIRT()
    task.ref_file = File.sample(seed=0)
    task.in_file = File.sample(seed=1)
    task.affine_file = File.sample(seed=2)
    task.inwarp_file = File.sample(seed=3)
    task.in_intensitymap_file = [File.sample(seed=4)]
    task.refmask_file = File.sample(seed=13)
    task.inmask_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_fnirt_2():
    task = FNIRT()
    task.warp_resolution = (6, 6, 6)
    task.in_fwhm = [8, 4, 2, 2]
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
