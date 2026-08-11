from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.complex import Complex
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_complex_1():
    task = Complex()
    task.complex_in_file = File.sample(seed=0)
    task.complex_in_file2 = File.sample(seed=1)
    task.real_in_file = File.sample(seed=2)
    task.imaginary_in_file = File.sample(seed=3)
    task.magnitude_in_file = File.sample(seed=4)
    task.phase_in_file = File.sample(seed=5)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
