from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.erode_image import ErodeImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_erodeimage_1():
    task = ErodeImage()
    task.minimum_filter = False
    task.kernel_file = File.sample(seed=3)
    task.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
