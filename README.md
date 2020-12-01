# Brev Rest

## Install

```
poetry add git+https://gitlab.com/tourmaline1/brev-rest.git
```

or

```
pip install git+https://gitlab.com/tourmaline1/brev-rest.git
```

## Example

See `tests/example_app`

See `tests/test_brev_rest.py` for spec

## Running Locally

```python
from brev_rest import app

app.run(app_path="tests/example_app")
```

## API Swagger Docs

http://127.0.0.1:8000/docs

## Run Tests

```
pytest
```
