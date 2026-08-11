from fileformats.generic import Directory, File
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.fix.classifier import Classifier
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_classifier_1():
    task = Classifier()
    task.mel_ica = Directory.sample(seed=0)
    task.trained_wts_file = File.sample(seed=1)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
