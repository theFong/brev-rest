# Brev Rest

- [x] route details
- [x] sub routes
- [x] ApiRouter
- [ ] Brev Router accepts fastapi Router parameters
- [ ] Implement type hints/auto complete for decorator & Router
- [ ] Allow config of global app

## Example

See `tests/example_app`

See `tests/test_brev_rest.py` for spec

## Running Locally

```python
from brev_rest import app

app.run(app_path="tests/example_app")
```

### API Swagger Docs

http://127.0.0.1:8000/docs
