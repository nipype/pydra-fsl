from fileformats.generic import File
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.eddy_quad import EddyQuad
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_eddyquad_1():
    task = EddyQuad()
    task.base_name = "eddy_corrected"
    task.idx_file = File.sample(seed=1)
    task.param_file = TextFile.sample(seed=2)
    task.mask_file = File.sample(seed=3)
    task.bval_file = File.sample(seed=4)
    task.bvec_file = File.sample(seed=5)
    task.field = File.sample(seed=7)
    task.slice_spec = File.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddyquad_2():
    task = EddyQuad()
    task.param_file = TextFile.sample(seed=2)
    task.output_dir = "eddy_corrected.qc"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
