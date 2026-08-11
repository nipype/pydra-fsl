from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.overlay import Overlay
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_overlay_1():
    task = Overlay()
    task.transparency = True
    task.out_type = "float"
    task.background_image = File.sample(seed=3)
    task.stat_image = File.sample(seed=7)
    task.stat_image2 = File.sample(seed=10)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
