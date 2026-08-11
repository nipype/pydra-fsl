from fileformats.datascience import TextMatrix
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.vest_2_text import Vest2Text
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_vest2text_1():
    task = Vest2Text()
    task.in_file = TextMatrix.sample(seed=0)
    task.out_file = "design.txt"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_vest2text_2():
    task = Vest2Text()
    task.in_file = TextMatrix.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
