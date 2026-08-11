from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.ar1_image import AR1Image
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ar1image_1():
    task = AR1Image()
    task.dimension = "T"
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
