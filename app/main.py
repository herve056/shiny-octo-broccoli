"""FastAPI app to handle encryption and signing of data."""
import os
import sys
from fastapi import FastAPI, Response, HTTPException, Body
from .services.encoder import EncoderBase64
from .services.signer import SignerHMAC


app = FastAPI(title="Riot Take-home Api", version="0.1.0")

if "SECRET_KEY" not in os.environ:
    print("WARNING: SECRET_KEY environment variable is not set. Using default key, which is insecure for production.", file=sys.stderr)
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key").encode()
ENCODER = EncoderBase64()
SIGNER = SignerHMAC(SECRET_KEY)


@app.post("/encrypt",
    summary="Encrypt data",
    description="Encrypts all properties at depth 1 in the provided JSON object using Base64 encoding.",
    responses={
        200: {
            "description": "Successfully encrypted data",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Sm9obiBEb2U=",
                        "age": "MzA=",
                        "contact": (
                            "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9"
                        )
                    }
                }
            }
        }
    }
)
async def encrypt(
    data: dict = Body(
        openapi_examples={
            "An normal example": {
                "summary": "A normal example",
                "value": {
                    "name": "John Doe",
                    "age": 30,
                    "contact": {
                        "email": "john@example.com",
                        "phone": "123-456-7890"
                    }
                },
            }
        }
    )
):
    return {key: ENCODER.encode(value) for key, value in data.items()}


@app.post("/decrypt",
    summary="Decrypt data",
    description=(
        "Decrypts all properties at depth 1 in the provided JSON object using Base64 encoding. "
        "If some properties contain values which were not encrypted, they remain unchanged."
    ),
    responses={
        200: {
            "description": "Successfully decrypted data",
            "content": {
                "application/json": {
                    "example": {
                        "name": "John Doe",
                        "age": 30,
                        "contact": {
                            "email": "john@example.com",
                            "phone": "123-456-7890"
                        }
                    }
                }
            }
        }
    }
)
async def decrypt(
    data: dict = Body(
        openapi_examples={
            "An normal example": {
                "summary": "A normal example",
                "value": {
                    "name": "Sm9obiBEb2U=",
                    "age": "MzA=",
                    "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9"
                }
            }
        }
    )
):
    return {key: ENCODER.decode(value) for key, value in data.items()}


@app.post("/sign",
    summary="Sign data",
    description=(
        "Signs the provided JSON object using HMAC algorithm. "
        "The signature is computed over the canonicalized JSON representation, "
        "ensuring that property order does not affect the signature."
    ),
    responses={
        200: {
            "description": "JSON payload with a unique \"signature\" property in hexadecimal format.",
            "content": {
                "application/json": {
                    "example": {
                      "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28"
                    }
                }
            }
        }
    }
)
async def sign(
    data: dict = Body(
        openapi_examples={
            "An normal example": {
                "summary": "A normal example",
                "value": {
                    "message": "Hello World",
                    "timestamp": 1616161616
                }
            }
        }
    )
):
    return {"signature": SIGNER.sign(data)}


@app.post("/verify",
    summary="Verify signature",
    description="Verifies the provided JSON object's signature using HMAC algorithm.",
    responses={
        204: {
            "description": "No content if the signature is valid.",
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid signature"
                    }
                }
            }
        }
    },
    status_code=204  # Explicitly set the default status code to 204
)
async def verify(
    data: dict = Body(
        openapi_examples={
            "An normal example": {
                "summary": "A normal example",
                "value": {
                    "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28",
                    "data": {
                        "message": "Hello World",
                        "timestamp": 1616161616
                    }
                }
            }
        }
    )
):
    signed_data = data.get("data")
    if not signed_data:
        raise HTTPException(status_code=400, detail="Data to verify is required")
    signature = data.get("signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Signature is required")
    if SIGNER.verify(signed_data, signature):
        return Response(status_code=204)
    raise HTTPException(status_code=400, detail="Invalid signature")
