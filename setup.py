"""
    Setup file for julia_brot.
    Use setup.cfg to configure the project.
"""
import pathlib

from setuptools import Extension, setup

try:
    from Cython.Build import cythonize, build_ext
except ImportError:
    cythonize = None

if __name__ == "__main__":
    try:
        cmdclass = {}
        extensions = {
            "julia": "src/julia_brot/julia.c",
            "mandelbrot": "src/julia_brot/mandelbrot.c",
        }
        CYTHONIZE = True
        for name, file in extensions.items():
            if pathlib.Path(file).exists():
                CYTHONIZE = False
                break
        if CYTHONIZE:
            for name, file in extensions.items():
                extensions[name] = file.replace(".c", ".pyx")
            cmdclass.update({"build_ext": build_ext})
        extensions = [
            Extension(f"julia_brot.{name}", [file]) for name, file in extensions.items()
        ]
        if CYTHONIZE:
            extensions = cythonize(extensions)
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            ext_modules=extensions,
            cmdclass=cmdclass,
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
