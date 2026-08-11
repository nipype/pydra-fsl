from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.filter_regressor import FilterRegressor
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_filterregressor_1():
    task = FilterRegressor()
    task.in_file = File.sample(seed=0)
    task.design_file = File.sample(seed=2)
    task.mask = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
