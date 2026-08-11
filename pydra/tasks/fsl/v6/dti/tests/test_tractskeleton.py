from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.tract_skeleton import TractSkeleton
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_tractskeleton_1():
    task = TractSkeleton()
    task.in_file = File.sample(seed=0)
    task.distance_map = File.sample(seed=3)
    task.search_mask_file = File.sample(seed=4)
    task.use_cingulum_mask = True
    task.data_file = File.sample(seed=6)
    task.alt_data_file = File.sample(seed=7)
    task.alt_skeleton = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
