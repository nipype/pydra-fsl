from fileformats.datascience import TextMatrix
from fileformats.generic import File
from fileformats.medimage import Nifti1
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.prob_track_x import ProbTrackX
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_probtrackx_1():
    task = ProbTrackX()
    task.mask2 = File.sample(seed=1)
    task.mesh = File.sample(seed=2)
    task.thsamples = [Nifti1.sample(seed=3)]
    task.phsamples = [Nifti1.sample(seed=4)]
    task.fsamples = [Nifti1.sample(seed=5)]
    task.samples_base_name = "merged"
    task.mask = Nifti1.sample(seed=7)
    task.target_masks = [Nifti1.sample(seed=9)]
    task.waypoints = File.sample(seed=10)
    task.seed_ref = File.sample(seed=12)
    task.force_dir = True
    task.opd = True
    task.avoid_mp = File.sample(seed=18)
    task.stop_mask = File.sample(seed=19)
    task.xfm = TextMatrix.sample(seed=20)
    task.inv_xfm = File.sample(seed=21)
    task.n_samples = 5000
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_probtrackx_2():
    task = ProbTrackX()
    task.mode = "seedmask"
    task.thsamples = [Nifti1.sample(seed=3)]
    task.phsamples = [Nifti1.sample(seed=4)]
    task.fsamples = [Nifti1.sample(seed=5)]
    task.samples_base_name = "merged"
    task.mask = Nifti1.sample(seed=7)
    task.seed = "MASK_average_thal_right.nii"
    task.target_masks = [Nifti1.sample(seed=9)]
    task.out_dir = "."
    task.force_dir = True
    task.opd = True
    task.os2t = True
    task.xfm = TextMatrix.sample(seed=20)
    task.n_samples = 3
    task.n_steps = 10
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
