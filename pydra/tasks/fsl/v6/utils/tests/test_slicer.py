from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.slicer import Slicer
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_slicer_1():
    task = Slicer()
    task.in_file = File.sample(seed=0)
    task.image_edges = File.sample(seed=1)
    task.label_slices = True
    task.colour_map = File.sample(seed=3)
    task.show_orientation = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
