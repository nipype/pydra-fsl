from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.av_scale import AvScale
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_avscale_1():
    task = AvScale()
    task.mat_file = File.sample(seed=1)
    task.ref_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
