from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.filmgls import FILMGLS
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_filmgls_1():
    task = FILMGLS()
    task.in_file = File.sample(seed=0)
    task.design_file = File.sample(seed=1)
    task.threshold = 1000.0
    task.results_dir = "results"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
