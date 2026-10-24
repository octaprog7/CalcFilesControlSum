# Changelog

All notable changes to the CalcFilesControlSum project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-10-24

### Added
- [`__init__.py`](src/calc_files_control_sum/__init__.py): package docstring, relative imports of submodules, re-exports of the public API (`Config`, `ConfigReader`, `ConfigWriter`), `__version__ = "1.2.0"`, and an `__all__` list.

### Changed
- The report file format (`*.cs`) is now locale-independent: the statistics lines in the `INFO` section (`Work completed`, `Number of files`, `Bytes processed`, `Processing speed [MiB/s]`) were moved from the localized `my_strings` into the "no translation" module [`str_without_trans.py`](src/calc_files_control_sum/str_without_trans.py). Reports are now identical on any system (previously these lines were translated to the OS language).
- `ConfigReader.read()`: proper typing via `@overload` — when called with a section name the type stays `Iterable[tuple[str, str]]`; when reading the whole file the honest type is `Iterable[tuple[str, str | None] | str]` (the static analyzer warning about yielding a `str` was resolved).

### Fixed
- `make_check_file`: the invocation was aligned with the actual project layout (`src`-layout) and with the installed console command `cfcs`.
- `setup.py`: `python_requires='>=3.10'` — the actual minimum Python version (due to `A | B` type annotation syntax, PEP 604); the erroneous upper bound `<3.12` was removed, which previously prevented installation on Python 3.13.
- The local virtual environment `venv` was recreated on the current Python version (it previously pointed to a removed Python 3.9).

### Removed
- From [`my_strings.py`](src/calc_files_control_sum/my_strings.py): the now unused variables `strEnded`, `strFiles`, `strBytesProcessed`, `strProcSpeed` (their translations remain in `translated.csv`).

### Notes
- Version `1.2.0` is installed locally: globally via `pip install --user --break-system-packages .`, available as the console command `cfcs`.

## [Earlier versions]

A changelog was not maintained for versions prior to `1.2.0`.
Release history can be found on PyPI: <https://pypi.org/project/calc-files-control-sum/>
