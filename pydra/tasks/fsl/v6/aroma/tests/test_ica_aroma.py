from fileformats.generic import Directory, File
from fileformats.medimage import Nifti1, NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.aroma.ica__aroma import ICA_AROMA
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_ica_aroma_1():
    task = ICA_AROMA()
    task.feat_dir = Directory.sample(seed=0)
    task.in_file = Nifti1.sample(seed=1)
    task.out_dir = "out"
    task.mask = NiftiGz.sample(seed=3)
    task.melodic_dir = Directory.sample(seed=6)
    task.mat_file = File.sample(seed=7)
    task.fnirt_warp_file = Nifti1.sample(seed=8)
    task.motion_parameters = File.sample(seed=9)
    task.denoise_type = "nonaggr"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_ica_aroma_2():
    task = ICA_AROMA()
    task.in_file = Nifti1.sample(seed=1)
    task.out_dir = "ICA_testout"
    task.mask = NiftiGz.sample(seed=3)
    task.fnirt_warp_file = Nifti1.sample(seed=8)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
