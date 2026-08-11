from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.image_stats import ImageStats
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_imagestats_1():
    task = ImageStats()
    task.in_file = File.sample(seed=1)
    task.mask_file = File.sample(seed=3)
    task.index_mask_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagestats_2():
    task = ImageStats()
    task.in_file = File.sample(seed=1)
    task.op_string = "-M"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
