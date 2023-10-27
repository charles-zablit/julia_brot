==========
julia_brot
==========


    Fast Python CLI Library for plotting the Mandelbrot and Julia sets.


This project uses multi-threaded Cython to compute the representation of the Mandelbrot and Julia sets.


.. _pyscaffold-notes:

Installation
====

Install from release (recommended)
----
1. Download the latest wheel release from the `releases page <https://github.com/charles-zablit/julia_brot/releases/>`_ for your platform. If your platform is not listed, please see below to install from source.
2. Run pip install on it::

   pip install <path-to-whl>

Install from source
----
Clone the repository::

   git clone https://github.com/charles-zablit/julia_brot.git

Install `tox` from Pypi::

   pip install tox

Build the project::

   tox -e build

Get the path of the `.whl` file in the newly generated `dist` folder::

   ls dist/

Install the wheel like you would do for anyother library::

   pip install <path_to_wheel>


Documentation
====

https://charles-zablit.github.io/julia_brot/

Examples
====

Mandelbrot
----
.. image:: images/mandelbrot.png

Julia
----
.. image:: images/julia.png


CLI usage Examples
====

Generate a Mandelbrot image::

   $ MandelbrotPlot --zmin=-0.7440+0.1305j\
                --zmax=-0.7425+0.1320j \
                --pixel_size=5e-7\
                --max-iter=50\
                -o "Mandelbrot_tentacle_lowiter.png"

Generate a Julia image::

   $ JuliaPlot -c=-0.8j\
            --pixel_size=1e-3\
            --max-iter=50\
            -o "thunder-julia.png"

Parameters details::

   usage: MandelBrotPlot [-h] [-c [C]] [--zmin [ZMIN]] [--zmax [ZMAX]] [--pixel_size [PIXEL_SIZE]]
                      [--max-iter [MAX_ITER]] [-o [OUTPUT]] [-d]

   Mandelbrot plotting CLI.

   options:
     -h, --help            show this help message and exit
     -c [C], --c [C]       Initial value of the Julia set plot (ex: -1-1.5j)
     --zmin [ZMIN]         Lower bound of the plot, as a complex number (ex: -2-2j)
     --zmax [ZMAX]         Upper bound of the plot, as a complex number (ex: 2+2j)
     --pixel_size [PIXEL_SIZE]
                           Pixel size of the generated plot. The thigher the plot, the smaller this number
                           should be.
     --max-iter [MAX_ITER]
                           Number of iterations to generate the set.
     -o [OUTPUT], --output [OUTPUT]
                           Output path of the generated plot.
     -d, --debug           Set logging level to DEBUG


Running the tests
====

With `tox` installed, you can run the tests from the root of the project using the following command::

    tox
