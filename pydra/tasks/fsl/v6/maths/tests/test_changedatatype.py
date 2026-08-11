from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.maths.change_data_type import ChangeDataType
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_changedatatype_1():
    task = ChangeDataType()
    task.in_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
