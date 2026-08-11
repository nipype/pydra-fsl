from fileformats.generic import Directory, File
from fileformats.medimage import Bval, Bvec, Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.bedpostx5 import BEDPOSTX5
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_bedpostx5_1():
    task = BEDPOSTX5()
    task.dwi = Nifti1.sample(seed=0)
    task.mask = Nifti1.sample(seed=1)
    task.bvecs = Bvec.sample(seed=2)
    task.bvals = Bval.sample(seed=3)
    task.logdir = Directory.sample(seed=4)
    task.n_fibres = 2
    task.n_jumps = 5000
    task.burn_in = 0
    task.sample_every = 1
    task.out_dir = Directory.sample(seed=11)
    task.grad_dev = File.sample(seed=13)
    task.burn_in_no_ard = 0
    task.update_proposal_every = 40
    task.force_dir = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_bedpostx5_2():
    task = BEDPOSTX5()
    task.dwi = Nifti1.sample(seed=0)
    task.mask = Nifti1.sample(seed=1)
    task.bvecs = Bvec.sample(seed=2)
    task.bvals = Bval.sample(seed=3)
    task.n_fibres = 1
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
