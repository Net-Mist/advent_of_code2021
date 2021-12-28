from setuptools import Extension, setup

# cython need to be loaded after setuptools
from Cython.Build import cythonize  # noqa: E402 isort:skip

extra_compile_args = ["-O3", "-ffast-math", "-march=native"]

# see https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives
# for compiler directive
# see https://cython.readthedocs.io/en/latest/src/tutorial/strings.html#auto-encoding-and-decoding
# for string encoding in C/C++
compiler_directives = {
    "infer_types": True,
    "profile": True,
    "c_string_type": "str",
    "c_string_encoding": "ascii",
    "boundscheck": False,
    "wraparound": False,
    "nonecheck": False,
    "embedsignature": True,
}

extensions = [
    Extension("day15.module_c", ["day15/module.pyx"], extra_compile_args=extra_compile_args),
    Extension("day17.module_c", ["day17/module_c.pyx"], language="c++", extra_compile_args=extra_compile_args),
    Extension("day17.module_c2", ["day17/module.py"], language="c++", extra_compile_args=extra_compile_args),
    Extension("day18.module_c", ["day18/module_c.pyx"], language="c++", extra_compile_args=extra_compile_args),
    Extension("day19.module_c", ["day19/module_c.pyx"], language="c++", extra_compile_args=extra_compile_args),
    Extension("day20.module_c", ["day20/module_c.pyx"], language="c++", extra_compile_args=extra_compile_args),
    Extension("day23.module_c", ["day23/module.py"], extra_compile_args=extra_compile_args),
    Extension("day25.module_c", ["day25/module.py"], extra_compile_args=extra_compile_args),
]


setup(ext_modules=cythonize(extensions, language_level="3", compiler_directives=compiler_directives, annotate=True))
