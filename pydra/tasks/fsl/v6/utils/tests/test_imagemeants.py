from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.image_meants import ImageMeants
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_imagemeants_1():
    task = ImageMeants()
    task.in_file = File.sample(seed=0)
    task.mask = File.sample(seed=2)
    task.order = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
