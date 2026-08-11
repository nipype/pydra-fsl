from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.vec_reg import VecReg
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_vecreg_1():
    task = VecReg()
    task.in_file = Nifti1.sample(seed=0)
    task.ref_vol = Nifti1.sample(seed=2)
    task.affine_mat = TextMatrix.sample(seed=3)
    task.warp_field = File.sample(seed=4)
    task.rotation_mat = File.sample(seed=5)
    task.rotation_warp = File.sample(seed=6)
    task.mask = File.sample(seed=8)
    task.ref_mask = File.sample(seed=9)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_vecreg_2():
    task = VecReg()
    task.in_file = Nifti1.sample(seed=0)
    task.out_file = "diffusion_vreg.nii"
    task.ref_vol = Nifti1.sample(seed=2)
    task.affine_mat = TextMatrix.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
