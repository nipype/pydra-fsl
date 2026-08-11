from fileformats.generic import File
from fileformats.medimage import Nifti1
from fileformats.text import TextFile
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.epi.eddy import Eddy
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_eddy_1():
    task = Eddy()
    task.in_file = Nifti1.sample(seed=0)
    task.in_mask = File.sample(seed=1)
    task.in_index = TextFile.sample(seed=2)
    task.in_acqp = File.sample(seed=3)
    task.in_bvec = File.sample(seed=4)
    task.in_bval = File.sample(seed=5)
    task.out_base = "eddy_corrected"
    task.session = File.sample(seed=7)
    task.in_topup_fieldcoef = File.sample(seed=8)
    task.in_topup_movpar = File.sample(seed=9)
    task.field = File.sample(seed=10)
    task.field_mat = File.sample(seed=11)
    task.flm = "quadratic"
    task.slm = "none"
    task.interp = "spline"
    task.nvoxhp = 1000
    task.fudge_factor = 10.0
    task.niter = 5
    task.method = "jac"
    task.slice_order = TextFile.sample(seed=36)
    task.json = File.sample(seed=37)
    task.num_threads = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_2():
    task = Eddy()
    task.in_file = Nifti1.sample(seed=0)
    task.in_index = TextFile.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_3():
    task = Eddy()
    task.use_cuda = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_eddy_4():
    task = Eddy()
    task.mporder = 6
    task.slice2vol_lambda = 1
    task.slice_order = TextFile.sample(seed=36)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
