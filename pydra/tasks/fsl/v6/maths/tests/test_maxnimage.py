from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.maxn_image import MaxnImage
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_maxnimage_1():
    task = MaxnImage()
    task.dimension = "T"
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
