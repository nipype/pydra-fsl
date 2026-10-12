from fileformats.datascience import TextMatrix
from fileformats.generic import Directory, File
from fileformats.medimage import NiftiGz
from fileformats.vendor.fsl.medimage import Con
import logging
from nipype2pydra.testing import PassAfterTimeoutWorker
from pydra.tasks.fsl.v6.model.flameo import FLAMEO
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.xfail
def test_flameo_1():
    task = FLAMEO()
    task.cope_file = NiftiGz.sample(seed=0)
    task.var_cope_file = File.sample(seed=1)
    task.dof_var_cope_file = File.sample(seed=2)
    task.mask_file = File.sample(seed=3)
    task.design_file = File.sample(seed=4)
    task.t_con_file = Con.sample(seed=5)
    task.f_con_file = File.sample(seed=6)
    task.cov_split_file = TextMatrix.sample(seed=7)
    task.log_dir = Directory.sample(seed=17)
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)


@pytest.mark.xfail
def test_flameo_2():
    task = FLAMEO()
    task.cope_file = NiftiGz.sample(seed=0)
    task.t_con_file = Con.sample(seed=5)
    task.cov_split_file = TextMatrix.sample(seed=7)
    task.run_mode = "fe"
    print(f"CMDLINE: {task.cmdline}\n\n")
    res = task(worker=PassAfterTimeoutWorker)
    print("RESULT: ", res)
