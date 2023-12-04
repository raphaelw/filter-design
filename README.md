# emqf-filter-design

[![Python package](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml/badge.svg)](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml)

SciPy compatible design tools around Elliptic Filters with minimal Q-factors (EMQF)

## How to contribute

Install this library in editable mode:

```sh
pip install -e .
```

Or install with all optional dependencies
```sh
pip install -e .[examples,dev,build]
```

Run tests

```sh
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

Use [Black](https://github.com/psf/black) Code Formatter.