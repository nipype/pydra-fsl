from fileformats.generic import File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.utils.copy_geom import CopyGeom
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_copygeom_1():
    task = CopyGeom()
    task.in_file = File.sample(seed=0)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
