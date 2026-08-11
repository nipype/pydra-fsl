from fileformats.generic import Directory
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.fix.training_set_creator import TrainingSetCreator
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_trainingsetcreator_1():
    task = TrainingSetCreator()
    task.mel_icas_in = [Directory.sample(seed=0)]
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
