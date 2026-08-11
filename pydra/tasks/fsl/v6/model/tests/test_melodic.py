from fileformats.generic import File
from fileformats.vendor.fsl.medimage import Con
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.melodic import MELODIC
import pytest


logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_melodic_1():
    task = MELODIC()
    task.in_files = [File.sample(seed=0)]
    task.mask = File.sample(seed=2)
    task.ICs = File.sample(seed=27)
    task.mix = File.sample(seed=28)
    task.smode = File.sample(seed=29)
    task.bg_image = File.sample(seed=32)
    task.t_des = File.sample(seed=35)
    task.t_con = Con.sample(seed=36)
    task.s_des = File.sample(seed=37)
    task.s_con = Con.sample(seed=38)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_melodic_2():
    task = MELODIC()
    task.no_bet = True
    task.approach = "tica"
    task.tr_sec = 1.5
    task.t_con = Con.sample(seed=36)
    task.s_con = Con.sample(seed=38)
    task.out_stats = True
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
