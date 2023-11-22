from pathlib import Path
import typing as ty
from random import Random
from fileformats.core import FileSet
from fileformats.medimage_fsl import (
    Con,
)



@FileSet.generate_sample_data.register
def gen_sample_con_data(con: Con, dest_dir: Path, seed: ty.Union[int, Random], stem: ty.Optional[str]):
    raise NotImplementedError
