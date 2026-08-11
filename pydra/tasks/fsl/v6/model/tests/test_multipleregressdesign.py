import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.multiple_regress_design import MultipleRegressDesign
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_multipleregressdesign_1():
    task = MultipleRegressDesign()
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
