import pytest
from fileformats.medimage_fsl import (
    Con,
)



@pytest.mark.xfail(reason="generate_sample_data not implemented")
def test_generate_sample_con_data():
    assert isinstance(Con.sample(), Con)
