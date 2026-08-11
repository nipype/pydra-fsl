from ._version import __version__  # noqa: F401
from pathlib import Path
import typing as ty
from random import Random
from fileformats.core import FileSet, SampleFileGenerator
from fileformats.vendor.fsl.medimage import (
    Con,
)


@FileSet.generate_sample_data.register
def gen_sample_con_data(con: Con, generator: SampleFileGenerator) -> ty.Iterable[Path]:
    raise NotImplementedError
