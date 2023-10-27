import cython
import numpy as np
from cython.parallel import prange

from libc.stdlib cimport free, malloc


@cython.boundscheck(False)
@cython.wraparound(False)
def fast_julia(double complex c, double complex zmin, double complex zmax, double pixel_size, int max_iter):
    cdef:
        double[:] x = np.arange(zmin.real, zmax.real, pixel_size)
        double[:] y = np.arange(zmin.imag, zmax.imag, pixel_size)
        int [:, ::1] julia = np.zeros((x.size, y.size), dtype = np.int32)
        double zr, zi
        double cr = c.real, ci = c.imag
        int  i, j, nx=x.size, ny=y.size
        int *ite

    for j in prange(ny, nogil=True, schedule='dynamic'):
        ite = <int *> malloc(sizeof(int))
        for i in range(nx):
            zr = x[i]
            zi = y[j]
            ite[0] = 0
            while (zr*zr + zi*zi) <= 2 and ite[0] < max_iter:
                zr, zi = zr*zr - zi*zi + cr, 2*zr*zi + ci
                ite[0] += 1
            julia[i, j] = ite[0]
        free(ite)

    return julia