from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.maths_command import MathsCommand
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_mathscommand_1():
    task = MathsCommand()
    task.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
