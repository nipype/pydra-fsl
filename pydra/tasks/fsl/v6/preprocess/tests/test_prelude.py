from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.prelude import PRELUDE
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_prelude_1():
    task = PRELUDE()
    task.complex_phase_file = File.sample(seed=0)
    task.magnitude_file = File.sample(seed=1)
    task.phase_file = File.sample(seed=2)
    task.mask_file = File.sample(seed=9)
    task.savemask_file = File.sample(seed=12)
    task.rawphase_file = File.sample(seed=13)
    task.label_file = File.sample(seed=14)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
