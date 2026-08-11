from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.temporal_filter import TemporalFilter
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_temporalfilter_1():
    task = TemporalFilter()
    task.lowpass_sigma = -1
    task.highpass_sigma = -1
    task.in_file = File.sample(seed=2)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
