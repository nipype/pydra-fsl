from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.distance_map import DistanceMap
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_distancemap_1():
    task = DistanceMap()
    task.in_file = File.sample(seed=0)
    task.mask_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
