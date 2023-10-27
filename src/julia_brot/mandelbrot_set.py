import logging
import sys
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from .common import _handle_img, _normalize, _parse_args, _setup_logging

from julia_brot.mandelbrot import fast_mandelbrot


def _fast_mandelbrot(zmin: complex, zmax: complex, pixel_size: float, max_iter: int):
    """Wrapper function around the Cython implementation of `fast_mandelbrot`.

    Parameters
    ----------
    zmin : complex
        Lower bound limit.
    zmax : complex
        Upper bound limit.
    pixel_size : float
        Pixel size of the resulting plot.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    np.ndarray
        Numpy array of the computed set with type `np.float32`
    """
    arr = fast_mandelbrot(zmin, zmax, pixel_size, max_iter)
    return np.asarray(arr).astype(np.float32)


def _generate_mandelbrot_img(
    zmin=-2 - 2j,
    zmax=2 + 2j,
    pixel_size=0.1,
    max_iter=600,
) -> Image:
    """Generate an `Image` of the Mandelbrot set.

    Parameters
    ----------
    zmin : complex
        Lower bound limit.
    zmax : complex
        Upper bound limit.
    pixel_size : float
        Pixel size of the resulting plot.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    Image
        Handle of the `Image`.
    """
    logging.debug(f"Generating a Mandelbrot set image.")
    arr = _fast_mandelbrot(zmin, zmax, pixel_size, max_iter)
    arr = 1 - _normalize(arr)
    cm = plt.get_cmap("inferno")
    arr = cm(arr.T)
    return Image.fromarray((arr[:, :, :3] * 255).astype(np.uint8))


def plot_mandelbrot(
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 600,
    figname: Optional[str] = None,
):
    """Plot the Mandelbrot set.

    Parameters
    ----------
    zmin : complex
        Lower bound limit.
    zmax : complex
        Upper bound limit.
    pixel_size : float
        Pixel size of the resulting plot.
    max_iter : int
        Maximum number of iterations.
    figname : Optional[Union[str, bytes, os.PathLike]]
        Optional path to save the plotted image to. Will not be saved if None.

    Example
    -------
    >>> plot_mandelbrot()
    None
    >>> plot_mandelbrot(
            zmin=-0.7440 + 0.1305j,
            zmax=-0.7425 + 0.1320j,
            pixel_size=5e-7,
            max_iter=200,
            figname=figname,
        )
    None
    """
    img = _generate_mandelbrot_img(zmin, zmax, pixel_size, max_iter)
    _handle_img(img, figname)


def is_in_mandelbrot(c: complex, max_iter: int = 10) -> bool:
    """Checks if a point is in the Mandelbrot set for a maximum number of iterations.

    Parameters
    ----------
    c : complex
        Point to check for.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    bool
        `True` if the point is in the set, `False` otherwise.

    Example
    -------
    >>> is_in_mandelbrot(c=0.251)
    True
    >>> is_in_mandelbrot(c=0.251, max_iter=100)
    False
    """
    z = 0
    for _ in range(max_iter):
        z = z**2 + c
    return abs(z) <= 2


def _plot_mandelbrot_cli():
    """Plot the Mandelbrot set and save it.
    This function is meant to be called from the CLI.
    """
    args = _parse_args(sys.argv[1:], "Mandelbrot")
    _setup_logging(args.loglevel)
    img = _generate_mandelbrot_img(args.zmin, args.zmax, args.pixel_size, args.max_iter)
    _handle_img(img, args.output)
