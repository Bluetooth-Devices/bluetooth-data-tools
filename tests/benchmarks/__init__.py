"""Benchmarks, shared by both CI benchmark runners.

The same modules are collected twice: CodSpeed drives them under
``pytest --codspeed`` (instrumentation mode), and pytest-benchmark drives
them under a plain ``pytest`` run (walltime, published to the job summary).
Whichever plugin owns the ``benchmark`` fixture for that run supplies it, so
one file serves both. Do not fork a second copy for the walltime runner --
a mirror drifts silently the moment either side is edited alone.
"""
