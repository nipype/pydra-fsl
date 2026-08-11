import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.level_1_design import Level1Design
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_level1design_1():
    task = Level1Design()
    task.orthogonalization = {}
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
