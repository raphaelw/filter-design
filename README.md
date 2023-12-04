# filter-design-toolkit

[![Python package](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml/badge.svg)](https://github.com/raphaelw/emqf-filter-design/actions/workflows/python-package.yml)

SciPy compatible design tools around Elliptic filters with minimal Q-factors (EMQF). EMQF filters are a subset of Elliptic IIR filters. They can be used for different purposes:
- Crossover filter pairs which can be used in real-time [audio filterbanks](https://doi.org/10.1109/78.469858)
    - Magnitude-complementary pairs aka [Generalized Linkwitz–Riley crossovers](https://www.native-instruments.com/fileadmin/ni_media/downloads/pdf/VAFilterDesign_2.1.0.pdf) (also [here](https://www.researchgate.net/profile/Ljiljana-Milic/publication/224633975_Magnitude_Complementary_Digital_Filter_Pairs_as_Loudspeaker_Crossovers/links/559fe43908ae5ab90245a34a/Magnitude-Complementary-Digital-Filter-Pairs-as-Loudspeaker-Crossovers.pdf))
    - Power-complementary pairs
- [Quadrature mirror filter (QMF)](https://en.wikipedia.org/wiki/Quadrature_mirror_filter) for Wavelet style filterbanks
- Efficient IIR Hilbert Transformer

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