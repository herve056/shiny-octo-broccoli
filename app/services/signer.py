"""Module providing an Signer abstraction and a HMAC signer implementation."""
import json
import hmac
import hashlib
from typing import Any
from abc import ABC, abstractmethod


class Signer(ABC):
    """Abstract base class for data signing/verification."""

    @abstractmethod
    def sign(self, data: Any) -> str:
        """
        Sign the data.
        Return a hex-encoded signature.
        """
        pass

    def verify(self, data: str, signature: str) -> bool:
        """
        Verify the signature of the data.
        """
        return hmac.compare_digest(signature, self.sign(data))


class SignerHMAC(Signer):
    """HMAC signer implementation."""

    def __init__(self, key: bytes):
        self.key = key

    def sign(self, data: Any) -> str:
        """
        Sign the data using HMAC with SHA256.
        Signing canonicalizes JSON by sorting object keys recursively and using compact separators, so object property order does not affect signatures.
        """
        json_data = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode()
        signature = hmac.new(self.key, json_data, hashlib.sha256).hexdigest()
        return signature
