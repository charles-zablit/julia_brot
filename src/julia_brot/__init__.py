from importlib.metadata import PackageNotFoundError  # pragma: no cover
from importlib.metadata import version

__author__ = "Charles Zablit"
__copyright__ = "Charles Zablit"
__license__ = "MIT"

try:
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .julia_set import is_in_julia, plot_julia
from .mandelbrot_set import is_in_mandelbrot, plot_mandelbrot

__all__ = ["plot_mandelbrot", "is_in_mandelbrot", "plot_julia", "is_in_julia"]
