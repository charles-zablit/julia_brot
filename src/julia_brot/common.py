import argparse
import logging
import os
import sys
from typing import List, Optional, Union

import numpy as np
from PIL.Image import Image


def _normalize(arr: np.ndarray) -> np.ndarray:
    """Normalize a numpy array between 0 and 1.

    Parameters
    ----------
    arr : np.ndarray
        Array to normalize.

    Returns
    -------
    np.ndarray
        Normalized array.
    """
    max_ = arr.max()
    min_ = arr.min()
    return (arr - min_) / (max_ - min_)


def _handle_img(img: Image, filename: Optional[Union[str, bytes, os.PathLike]]):
    """Save an `Image` if the `filename` is not None and then show it.

    Parameters
    ----------
    img : Image
        Handle to the `Image` to save and show.
    filename : Optional[Union[str, bytes, os.PathLike]]
        Path to save the image to. Will not save if None.
    """
    if filename is not None:
        logging.debug(f"Saving image to {filename}")
        img.save(filename, "PNG", quality=100, subsampling=0)
    img.show()


def _setup_logging(loglevel: int):
    """Setup some simple logging.

    Parameters
    ----------
    loglevel : int
        Loglevel to use, as provided by the `logging` module.
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%H:%M:%S.%f"
    )


def _parse_args(args: List[str], name: str) -> argparse.Namespace:
    """Parse command line arguments to be consumed for plotting the Mandelbrot and
    Julia set.

    Parameters
    ----------
    args : List[str]
        Raw arguments from the shell call.
    name : str
        Name of the set we will be plotting.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
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

    return parser.parse_args(args)
