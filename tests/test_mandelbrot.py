import pathlib
from unittest.mock import patch

import pytest

from julia_brot import is_in_mandelbrot, plot_mandelbrot

__author__ = "Charles Zablit"
__copyright__ = "Charles Zablit"
__license__ = "MIT"


def test_is_in_mandelbrot():
    """Test `is_in_mandelbrot`"""
    assert is_in_mandelbrot(c=0.251)
    assert not is_in_mandelbrot(c=0.251, max_iter=100)
    assert not is_in_mandelbrot(c=1 + 1j)
    assert not is_in_mandelbrot(c=10 + 10j)
    assert is_in_mandelbrot(c=0)


@patch("PIL.Image.Image.show")
def test_plot_mandelbrot(mock_show, tmp_path: pathlib.Path):
    """Test `plot_mandelbrot`"""
    assert plot_mandelbrot() is None
    figname = tmp_path.joinpath("Mandelbrot_tentacle.png")
    assert (
        plot_mandelbrot(
            zmin=-0.7440 + 0.1305j,
            zmax=-0.7425 + 0.1320j,
            pixel_size=5e-7,
            max_iter=200,
            figname=figname,
        )
        is None
    )
    assert figname.exists()
