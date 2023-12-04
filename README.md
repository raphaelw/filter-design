# emqf-filter-design

[![Python package](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml/badge.svg)](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml)

SciPy compatible design tools for Elliptic Filters with minimal Q-factors (EMQF)

## How to contribute

Install this library in editable mode:

```sh
pip install -e .
```

Run tests

```sh
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

## Other

Install with all optional dpendncies
```sh
pip install -e .[examples,dev,build]
```