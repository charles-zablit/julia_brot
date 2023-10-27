import pathlib
from unittest.mock import patch

import pytest

from julia_brot import is_in_julia, plot_julia

__author__ = "Charles Zablit"
__copyright__ = "Charles Zablit"
__license__ = "MIT"


def test_is_in_julia():
    """Test `is_in_julia`"""
    assert is_in_julia(z=0.25 + 0.25j, c=0.25)
    assert is_in_julia(z=0.25 + 0.25j, c=0.25, max_iter=100)
    assert not is_in_julia(z=1 + 1j, c=0.25)
    assert not is_in_julia(z=10 + 10j, c=0.25)
    assert is_in_julia(z=0, c=0)


@patch("PIL.Image.Image.show")
def test_plot_julia(mock_show, tmp_path: pathlib.Path):
    """Test `plot_julia`"""
    assert plot_julia() is None
    figname = tmp_path.joinpath("Julia_-0.8+0.156j.png")
    assert (
        plot_julia(
            c=-0.8 + 0.156j,
            zmin=-2 - 1j,
            zmax=2 + 1j,
            pixel_size=5e-4,
            max_iter=100,
            figname=figname,
        )
        is None
    )
    assert figname.exists()
