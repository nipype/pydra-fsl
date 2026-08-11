from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.spatial_filter import SpatialFilter
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_spatialfilter_1():
    task = SpatialFilter()
    task.kernel_file = File.sample(seed=3)
    task.in_file = File.sample(seed=4)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
