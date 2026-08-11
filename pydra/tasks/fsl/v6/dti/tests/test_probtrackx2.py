from fileformats.generic import File
from fileformats.medimage import NiftiGz
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.prob_track_x2 import ProbTrackX2
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_probtrackx2_1():
    task = ProbTrackX2()
    task.fopd = File.sample(seed=1)
    task.target2 = File.sample(seed=8)
    task.target3 = File.sample(seed=10)
    task.lrtarget3 = File.sample(seed=11)
    task.colmask4 = File.sample(seed=14)
    task.target4 = File.sample(seed=15)
    task.thsamples = [File.sample(seed=17)]
    task.phsamples = [File.sample(seed=18)]
    task.fsamples = [NiftiGz.sample(seed=19)]
    task.samples_base_name = "merged"
    task.mask = NiftiGz.sample(seed=21)
    task.target_masks = [File.sample(seed=23)]
    task.waypoints = File.sample(seed=24)
    task.seed_ref = File.sample(seed=26)
    task.force_dir = True
    task.opd = True
    task.avoid_mp = File.sample(seed=32)
    task.stop_mask = File.sample(seed=33)
    task.xfm = File.sample(seed=34)
    task.inv_xfm = File.sample(seed=35)
    task.n_samples = 5000
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_probtrackx2_2():
    task = ProbTrackX2()
    task.fsamples = [NiftiGz.sample(seed=19)]
    task.mask = NiftiGz.sample(seed=21)
    task.seed = "seed_source.nii.gz"
    task.n_samples = 3
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
