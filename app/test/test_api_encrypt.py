import os
import json
from fastapi.testclient import TestClient

if 'SECRET_KEY' in os.environ:
    del os.environ['SECRET_KEY']

from ..main import app


class TestApiEncrypt:

    def setup_class(self):
        self.client = TestClient(app)


    def test_encrypt_ok(self):
        response = self.client.post("/encrypt", json={
            "name": "John Doe",
            "age": 30,
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
            }
            })
        assert response.status_code == 200
        assert response.json() == {
            "name": "Sm9obiBEb2U=",
            "age": "MzA=",
            "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9"
            }


    def test_decrypt_ok(self):
        response = self.client.post("/decrypt", json={
            "name": "Sm9obiBEb2U=",
            "age": "MzA=",
            "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9"
            })
        assert response.status_code == 200
        assert response.json() == {
            "name": "John Doe",
            "age": 30,
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
                },
            }


    def test_encrypt_decrypt_cycle(self):
        message = '{"name": "John Doe", "age": 30,"contact": {"email": "john@example.com", "phone": "123-456-7890" }}'
        response = self.client.post("/encrypt", data=message)
        assert response.status_code == 200
        encrypted_data = response.text
        response = self.client.post("/decrypt", data=encrypted_data)
        assert response.status_code == 200
        assert response.json() == json.loads(message)


    def test_encrypt_empty(self):
        response = self.client.post("/encrypt", json={})
        assert response.status_code == 200
        assert response.json() == {}


    def test_decrypt_empty(self):
        response = self.client.post("/decrypt", json={})
        assert response.status_code == 200
        assert response.json() == {}


    def test_encrypt_bad_data(self):
        response = self.client.post("/encrypt", data="aaa")
        assert response.status_code == 422


    def test_decrypt_unencrypted_field(self):
        response = self.client.post("/decrypt", json={
            "name": "Sm9obiBEb2U=",
            "age": "MzA=",
            "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
            "birth_date": "1998-11-19" # This field is unencrypted
        })
        assert response.status_code == 200
        assert response.json() == {
            "name": "John Doe",
            "age": 30,
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890"
            },
            "birth_date": "1998-11-19"
        }
