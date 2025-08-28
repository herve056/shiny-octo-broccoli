"""Module providing an Encoder abstraction and a base64 encoder implementation."""

import json
import base64
from typing import Any
from abc import ABC, abstractmethod


class Encoder(ABC):
    """Abstract base class for data encoding/decoding."""

    @abstractmethod
    def encode(self, data: Any) -> str:
        """Encode the data."""
        pass

    @abstractmethod
    def decode(self, data: str) -> Any:
        """Decode the data."""
        pass


class EncoderBase64(Encoder):
    """Base64 encoder/decoder implementation."""

    def encode(self, data: Any) -> str:
        """
        Base64 encode the data.
        If the data is a string, it is encoded directly.
        If it is a JSON serializable object, it is first serialized to a JSON string.
        """
        if isinstance(data, str):
            data = data.encode()
        else:
            data = json.dumps(data, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode()
        return base64.b64encode(data).decode()

    def decode(self, data: str) -> Any:
        """
        Base64 decode the data if it is a base64 encoded string.
        If it is a JSON string, it is then deserialized to a Python object.
        """
        try:
            decoded_value = base64.b64decode(data, validate=True).decode()
        except (base64.binascii.Error, ValueError):
            decoded_value = data
        try:
            return json.loads(decoded_value)
        except json.JSONDecodeError:
            return decoded_value
