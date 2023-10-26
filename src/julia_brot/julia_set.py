from typing import Optional
import numpy as np
import itertools
from .common import _setup_logging, _make_fig, _parse_args, _init_space
import logging
import sys
import warnings


def _generate_julia_fig(
    c: complex = 0,
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 600,
):
    dpi = 150
    z = _init_space(zmin, zmax, pixel_size)
    w, h = zmax.imag - zmin.imag, zmax.real - zmin.real
    logging.debug(f"Generating a {z.shape[1]}x{z.shape[0]} Julia set plot.")
    julia = np.zeros(z.shape, dtype=np.int32)

    # Suppressing Numpy warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", r"(overflow|invalid value) encountered in")
        for ite in itertools.count():
            z = z**2 + c
            mask = np.logical_not(julia) & (np.abs(z) >= 400)
            julia[mask] = ite
            if np.all(julia) or ite > max_iter:
                break

    return _make_fig(julia, w, h, (zmin.real, zmax.real, zmin.imag, zmax.imag), dpi)


def plot_julia(
    c: complex = 0 + 0j,
    zmin: complex = -2 - 2j,
    zmax: complex = 2 + 2j,
    pixel_size: float = 0.1,
    max_iter: int = 2000,
    figname: Optional[str] = None,
):
    fig = _generate_julia_fig(c, zmin, zmax, pixel_size, max_iter)
    if figname is not None:
        logging.debug(f"Saving plot to {figname}")
        fig.savefig(figname, bbox_inches="tight")
    fig.show()


def _plot_julia_cli():
    args = _parse_args(sys.argv[1:], "Julia")
    _setup_logging(args.loglevel)
    fig = _generate_julia_fig(
        args.c, args.zmin, args.zmax, args.pixel_size, args.max_iter
    )
    logging.debug(f"Saving plot to {args.output}")
    fig.savefig(args.output, bbox_inches="tight")
