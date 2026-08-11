from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.dti.make_dyadic_vectors import MakeDyadicVectors
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_makedyadicvectors_1():
    task = MakeDyadicVectors()
    task.theta_vol = File.sample(seed=0)
    task.phi_vol = File.sample(seed=1)
    task.mask = File.sample(seed=2)
    task.output = File.sample(seed=3)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
