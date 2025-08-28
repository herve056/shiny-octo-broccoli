# Riot Take-Home Technical Challenge

## Project Description

This repository is an submission to the technical challenge described at [https://github.com/tryriot/take-home](https://github.com/tryriot/take-home).
It implements a FastAPI-based service for encoding, encryption, and signing of JSON data, providing endpoints for base64 encoding, HMAC signing, and signature verification.

## Features

FastAPI app exposes 4 endpoints:
- POST /encrypt: base64-encodes all depth-1 properties of a JSON object
- POST /decrypt: reverses /encrypt; unencrypted values remain unchanged
- POST /sign: returns an order-independent HMAC signature for any JSON
- POST /verify: validates signature against provided data

Api usage documentation is served at : /docs

## Directory Structure

```
├── app/
│   ├── main.py             # FastAPI app entry point
│   ├── services/
│   │   ├── encoder.py      # Base64 encoding logic
│   │   ├── signer.py       # HMAC signing logic
│   │   └── test/           # Unit tests for services
│   └── test/               # API endpoint tests
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Installation

```
python3 -m venv ./venv
source ./venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Tests

*Tested with Python 3.11*

Run tests:
```
pip install pytest
pytest
```

## Run locally

Set environment variable **SECRET_KEY** (default: "default-secret-key")

In fastapi dev environment :
```
fastapi dev --app app
```

Or run with uvicorn:
```
uvicorn app.main:app --reload
```

## Usage Example

Encrypt a JSON object:
```
curl -X POST "http://localhost:8000/encrypt" -H "Content-Type: application/json" -d '{"key": "value"}'
```

Others examples are shown in the API documentation [http://localhost:8000/docs](http://localhost:8000/docs).

## License

This project is provided for technical evaluation purposes. Please contact the maintainer for licensing details.

## Contact

Maintainer: herve056
For questions or support, open an issue or contact via GitHub.
