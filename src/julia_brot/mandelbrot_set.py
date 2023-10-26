import matplotlib.pyplot as plt
from typing import Optional
import sys
import logging
from .common import _setup_logging, _make_fig, _parse_args, _init_space
import warnings


def _generate_mandelbrot_fig(
    zmin=-2 - 2j,
    zmax=2 + 2j,
    pixel_size=0.1,
    max_iter=600,
) -> plt.Figure:
    dpi = 150
    c = _init_space(zmin, zmax, pixel_size)
    w, h = zmax.imag - zmin.imag, zmax.real - zmin.real
    z = 0
    logging.debug(f"Generating a {c.shape[1]}x{c.shape[0]} Mandelbrot set plot.")

    # Suppressing Numpy warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", r"(overflow|invalid value) encountered in")
        for n in range(max_iter):
            z = z**2 + c
        mandelbrot_set = abs(z) <= 2

    return _make_fig(
        mandelbrot_set, w, h, (zmin.real, zmax.real, zmin.imag, zmax.imag), dpi
    )

# def is_in_mandelbrot(c=0.251):


def plot_mandelbrot(
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 600,
    figname: Optional[str] = None,
):
    fig = _generate_mandelbrot_fig(zmin, zmax, pixel_size, max_iter)
    if figname is not None:
        logging.debug(f"Saving plot to {figname}")
        fig.savefig(figname, bbox_inches="tight")
    fig.show()


def _plot_mandelbrot_cli():
    args = _parse_args(sys.argv[1:], "Mandelbrot")
    _setup_logging(args.loglevel)
    fig = _generate_mandelbrot_fig(args.zmin, args.zmax, args.pixel_size, args.max_iter)
    logging.debug(f"Saving plot to {args.output}")
    fig.savefig(args.output, bbox_inches="tight")
