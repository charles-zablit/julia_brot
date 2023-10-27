import logging
import os
import sys
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

if os.getenv("DOCS_BUILD", 0) == 0:
    from julia_brot.julia import fast_julia

from .common import _handle_img, _normalize, _parse_args, _setup_logging


def _fast_julia(
    c: complex,
    zmin: complex,
    zmax: complex,
    pixel_size: float,
    max_iter: int,
) -> np.ndarray:
    """Wrapper function around the Cython implementation of `fast_julia`.

    Parameters
    ----------
    c : complex
        Julia constant.
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
    arr = fast_julia(c, zmin, zmax, pixel_size, max_iter)
    return np.asarray(arr).astype(np.float32)


def _generate_julia_img(
    c: complex = 0,
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 10,
) -> Image:
    """Generate an image of a Julia set.

    Parameters
    ----------
    c : complex
        Julia constant.
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
        Handle of the image.
    """
    logging.debug(f"Generating a Julia set image.")
    arr = _fast_julia(c, zmin, zmax, pixel_size, max_iter)
    arr = 1 - _normalize(arr)
    cm = plt.get_cmap("inferno")
    arr = cm(arr.T)
    return Image.fromarray((arr[:, :, :3] * 255).astype(np.uint8))


def plot_julia(
    c: complex = 0 + 0j,
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 10,
    figname: Optional[Union[str, bytes, os.PathLike]] = None,
):
    """Plot the Julia set corresponding to the given `c` constant.

    Parameters
    ----------
    c : complex
        Julia constant.
    zmin : complex
        Lower bound limit.
    zmax : complex
        Upper bound limit.
    pixel_size : float
        Pixel size of the resulting plot.
    max_iter : int
        Maximum number of iterations.
    figname : Optional[Union[str, bytes, os.PathLike]]
        Optional path to save the image to. Will not be saved if None.

    Example
    -------
    >>> plot_julia()
    None
    >>> plot_julia(c=-0.8 + 0.156j, zmin=-2-1j,
                   zmax=2+1j,
                   pixel_size=5e-4,
                   max_iter=100, figname=figname)
    None
    """
    img = _generate_julia_img(c, zmin, zmax, pixel_size, max_iter)
    _handle_img(img, figname)


def is_in_julia(z: complex, c: complex, max_iter: int = 10) -> bool:
    """Checks if a point is in a given Julia set for a maximum number of iterations.

    Parameters
    ----------
    z : complex
        Point to check for.
    c : complex
        Constant value of the Julia set.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    bool
        `True` if the point is in the set, `False` otherwise.

    Example
    -------
    >>> is_in_julia(z=0.25 + 0.25j, c=0.25)
    True
    >>> is_in_julia(z=0.25 + 0.25j, c=0.25, max_iter=100)
    True
    """
    for i in range(max_iter):
        z = z**2 + c
        if abs(z) > 2.0:
            return False
    return True


def _plot_julia_cli():
    """Plot the Julia set corresponding to the given `c` constant and save it.
    This function is meant to be called from the CLI.
    """
    args = _parse_args(sys.argv[1:], "Julia")
    _setup_logging(args.loglevel)
    img = _generate_julia_img(
        args.c, args.zmin, args.zmax, args.pixel_size, args.max_iter
    )
    _handle_img(img, args.output)
