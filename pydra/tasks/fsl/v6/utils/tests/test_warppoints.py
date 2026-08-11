from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.warp_points import WarpPoints
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_warppoints_1():
    task = WarpPoints()
    task.src_file = File.sample(seed=0)
    task.dest_file = Nifti1.sample(seed=1)
    task.in_coords = TextFile.sample(seed=2)
    task.xfm_file = File.sample(seed=3)
    task.warp_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_warppoints_2():
    task = WarpPoints()
    task.dest_file = Nifti1.sample(seed=1)
    task.in_coords = TextFile.sample(seed=2)
    task.coord_mm = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
