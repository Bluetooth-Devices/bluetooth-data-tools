"""Build optional cython modules."""

import os
import sys
import tempfile
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
    def usable_std_flag(self) -> str | None:
        """Return the C standard flag, or None if this compiler cannot use it.

        Not every toolchain that accepts ``-std=gnu2x`` implements C23: GCC 11
        and 12 set ``__STDC_VERSION__`` past C17 but do not provide ``nullptr``,
        which CPython 3.13+ ``pyport.h`` then uses -- and GCC below 11 rejects
        the flag outright. Compiling a probe against ``Python.h`` is the only
        reliable way to tell, so do that instead of guessing from a version.
        """
        flag = "/std:clatest" if self.compiler.compiler_type == "msvc" else "-std=gnu2x"
        with tempfile.TemporaryDirectory() as tmpdir:
            probe = join(tmpdir, "probe.c")
            with open(probe, "w") as handle:
                handle.write("#include <Python.h>\nint main(void) { return 0; }\n")
            try:
                self.compiler.compile(
                    [probe],
                    output_dir=tmpdir,
                    include_dirs=self.include_dirs,
                    extra_postargs=[flag],
                )
            except Exception:
                return None
        return flag

    def build_extensions(self) -> None:
        if self.parallel is None:  # type: ignore[has-type, unused-ignore]
            self.parallel = os.cpu_count() or 1
        std_flag = self.usable_std_flag()
        if std_flag is not None:
            for ext in self.extensions:
                if std_flag not in ext.extra_compile_args:
                    ext.extra_compile_args = [*ext.extra_compile_args, std_flag]
        try:
            super().build_extensions()
        except Exception:
            # A silent fallback here ships an extension-less wheel that only
            # fails much later (auditwheel) or not at all. Callers that need
            # the native modules opt into a hard failure.
            if os.environ.get("REQUIRE_CYTHON"):
                raise


def build(setup_kwargs: Any) -> None:
    if os.environ.get("SKIP_CYTHON", False):
        return
    try:
        from Cython.Build import cythonize  # noqa: PLC0415

        setup_kwargs.update(
            dict(
                ext_modules=cythonize(
                    [
                        # _time_impl cimports posix.time, so there is no
                        # sys/time.h to include on Windows. time.py only ever
                        # loads it on Linux; building it elsewhere is a
                        # guaranteed compile error.
                        *([] if sys.platform == "win32" else [time_module]),
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
