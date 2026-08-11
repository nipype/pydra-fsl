from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.min_image import MinImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_minimage_1():
    task = MinImage()
    task.dimension = "T"
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
