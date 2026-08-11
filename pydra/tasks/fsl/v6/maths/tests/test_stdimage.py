from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.std_image import StdImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_stdimage_1():
    task = StdImage()
    task.dimension = "T"
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
