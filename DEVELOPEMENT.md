# Developer guide

## How to do unit tests

```
pip install pytest
pytest
```
If you want to test a single module, run:
```
pytest tests/test_dump.py
```

## How to build and distribute

Navigate to the root of the project (where setup.py is located) and run the following commands:
```
pip install setuptools wheel
python setup.py sdist bdist_wheel
```
This will create a dist/ directory containing the source distribution and wheel files.

Then `stresscli` can be installed via pip:
```
pip install dist/stresscli-0.1-py3-none-any.whl
```
