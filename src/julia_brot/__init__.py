from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

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

from .mandelbrot_set import plot_mandelbrot
from .julia_set import plot_julia

__all__ = ["plot_mandelbrot", "plot_julia"]
