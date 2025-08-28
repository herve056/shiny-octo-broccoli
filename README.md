# Riot Take-Home Technical Challenge

## Features

FastAPI app exposes 4 endpoints:
- POST /encrypt: base64-encodes all depth-1 properties of a JSON object
- POST /decrypt: reverses /encrypt; unencrypted values remain unchanged
- POST /sign: returns an order-independent HMAC signature for any JSON
- POST /verify: validates signature against provided data

Api usage documentation is served at : /docs

## Installation

```
python3 -m venv ./venv
source ./venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

*Tested with Python 3.11*

## Tests

Run tests:
```
pip install pytest
pytest
```

### Run locally

Set environment variable **SECRET_KEY** (default: "default-secret-key")

In fastapi dev environment :
```
fastapi dev --app app
```

