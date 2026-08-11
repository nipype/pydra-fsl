from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.isotropic_smooth import IsotropicSmooth
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_isotropicsmooth_1():
    task = IsotropicSmooth()
    task.in_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
