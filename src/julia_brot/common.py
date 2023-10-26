import logging
import sys
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import argparse


def _normalize(arr) -> List[int]:
    max_ = max(arr)
    if max_ == 0:
        return arr
    return [e / max_ for e in arr]


def _init_space(zmin: complex, zmax: complex, pixel_size: float) -> np.ndarray:
    assert (
        zmax.imag - zmin.imag > 0
    ), f"Y axis boundaries are inverted. Got ymax={zmax.imag} < ymin={zmin.imag}"
    assert (
        zmax.real - zmin.real > 0
    ), f"X axis boundaries are inverted. Got xmax={zmax.real} < xmin={zmin.real}"
    w, h = zmax.imag - zmin.imag, zmax.real - zmin.real
    y = np.linspace(zmin.imag, zmax.imag, int(w / pixel_size))
    x = np.linspace(zmin.real, zmax.real, int(h / pixel_size))

    zx = x[np.newaxis, :]
    zy = y[:, np.newaxis]

    return zx + zy * 1j


def _make_fig(
    arr: np.ndarray,
    w: float,
    h: float,
    extent: Tuple[float, float, float, float],
    dpi=int,
):
    w, h = _normalize((w, h))
    figsize = (h * 15, w * 15)
    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    ax.imshow(
        arr,
        cmap="binary",
        extent=extent,
        interpolation="bicubic",
    )
    ax.axis("off")
    return fig


def _setup_logging(loglevel: int):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%H:%M:%S.%f"
    )


def _parse_args(args: List[str], name: str):
    parser = argparse.ArgumentParser(description=f"{name} plotting CLI.")
    parser.add_argument(
        "-c",
        "--c",
        help="Initial value of the Julia set plot (ex: -1-1.5j)",
        type=complex,
        nargs="?",
        default=0,
    )
    parser.add_argument(
        "--zmin",
        help="Lower bound of the plot, as a complex number (ex: -2-2j)",
        type=complex,
        nargs="?",
        default=-2 - 2j,
    )
    parser.add_argument(
        "--zmax",
        help="Upper bound of the plot, as a complex number (ex: 2+2j)",
        type=complex,
        nargs="?",
        default=2 + 2j,
    )
    parser.add_argument(
        "--pixel_size",
        help="Pixel size of the generated plot. The thigher the plot, the smaller this number should be.",
        type=float,
        nargs="?",
        default=1,
    )
    parser.add_argument(
        "--max-iter",
        help="Number of iterations to generate the set.",
        type=int,
        nargs="?",
        default=50,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path of the generated plot.",
        type=str,
        nargs="?",
        default="out.png",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Set logging level to DEBUG",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Set logging level to INFO",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    return parser.parse_args(args)
