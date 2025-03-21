"""Build optional cython modules."""

import os
from distutils.command.build_ext import build_ext
from os.path import join
from typing import Any

try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension

utils_module = Extension(
    "bluetooth_data_tools._utils_impl",
    [
        join("src", "bluetooth_data_tools", "_utils_impl.pyx"),
    ],
    language="c",
    extra_compile_args=["-O3", "-g0"],
)

time_module = Extension(
    "bluetooth_data_tools._time_impl",
    [
        join("src", "bluetooth_data_tools", "_time_impl.pyx"),
    ],
    language="c",
    extra_compile_args=["-O3", "-g0"],
)
TO_CYTHONIZE = [
    "src/bluetooth_data_tools/gap.py",
    "src/bluetooth_data_tools/utils.py",
]

EXTENSIONS = [
    Extension(
        ext.removeprefix("src/").removesuffix(".py").replace("/", "."),
        [ext],
        language="c",
        extra_compile_args=["-O3", "-g0"],
    )
    for ext in TO_CYTHONIZE
]


class BuildExt(build_ext):
    def build_extensions(self) -> None:
        try:
            super().build_extensions()
        except Exception:  # noqa: S110
            pass


def build(setup_kwargs: Any) -> None:
    if os.environ.get("SKIP_CYTHON", False):
        return
    try:
        from Cython.Build import cythonize

        setup_kwargs.update(
            dict(
                ext_modules=cythonize(
                    [
                        time_module,
                        utils_module,
                        *EXTENSIONS,
                    ],
                    compiler_directives={"language_level": "3"},  # Python 3
                ),
                cmdclass=dict(build_ext=BuildExt),
            )
        )
        setup_kwargs["exclude_package_data"] = {
            pkg: ["*.c"] for pkg in setup_kwargs["packages"]
        }
    except Exception:
        if os.environ.get("REQUIRE_CYTHON"):
            raise
        pass
