from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.preprocess.apply_xfm import ApplyXFM
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_applyxfm_1():
    task = ApplyXFM()
    task.apply_xfm = True
    task.in_file = File.sample(seed=1)
    task.reference = File.sample(seed=2)
    task.in_matrix_file = File.sample(seed=6)
    task.schedule = File.sample(seed=29)
    task.ref_weight = File.sample(seed=30)
    task.in_weight = File.sample(seed=31)
    task.wm_seg = File.sample(seed=38)
    task.wmcoords = File.sample(seed=39)
    task.wmnorms = File.sample(seed=40)
    task.fieldmap = File.sample(seed=41)
    task.fieldmapmask = File.sample(seed=42)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
