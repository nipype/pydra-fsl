from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.image_maths import ImageMaths
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_imagemaths_1():
    task = ImageMaths()
    task.in_file = File.sample(seed=0)
    task.in_file2 = File.sample(seed=1)
    task.mask_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_imagemaths_2():
    task = ImageMaths()
    task.in_file = File.sample(seed=0)
    task.out_file = "foo_maths.nii"
    task.op_string = "-add 5"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
