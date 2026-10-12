from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.vendor.fsl.medimage import Con
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.randomise import Randomise
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_randomise_1():
    task = Randomise()
    task.in_file = Nifti1.sample(seed=0)
    task.base_name = "randomise"
    task.design_mat = TextMatrix.sample(seed=2)
    task.tcon = Con.sample(seed=3)
    task.fcon = File.sample(seed=4)
    task.mask = Nifti1.sample(seed=5)
    task.x_block_labels = File.sample(seed=6)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_randomise_2():
    task = Randomise()
    task.in_file = Nifti1.sample(seed=0)
    task.design_mat = TextMatrix.sample(seed=2)
    task.tcon = Con.sample(seed=3)
    task.mask = Nifti1.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
