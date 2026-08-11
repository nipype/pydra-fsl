from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.cluster import Cluster
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_cluster_1():
    task = Cluster()
    task.in_file = File.sample(seed=0)
    task.cope_file = File.sample(seed=12)
    task.fractional = False
    task.use_mm = False
    task.find_min = False
    task.no_table = False
    task.minclustersize = False
    task.xfm_file = File.sample(seed=21)
    task.std_space_file = File.sample(seed=22)
    task.warpfield_file = File.sample(seed=24)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_cluster_2():
    task = Cluster()
    task.threshold = 2.3
    task.out_localmax_txt_file = "stats.txt"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
