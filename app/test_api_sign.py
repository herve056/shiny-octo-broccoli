from fastapi.testclient import TestClient
from .main import app


class TestApiSign:
    
    def setup_class(self):
        self.client = TestClient(app)


    def test_sign_ok(self):
        response = self.client.post("/sign", json={
            "message": "Hello World",
            "timestamp": 1616161616
        })
        assert response.status_code == 200
        assert response.json() == {
            "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28"
        }


    def test_verify_ok(self):
        response = self.client.post("/verify", json={
            "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28",
            "data": {
                "message": "Hello World",
                "timestamp": 1616161616
            }
        })
        assert response.status_code == 204


    def test_sign_different_order(self):
        response1 = self.client.post("/sign", data='{"message": "Hello World","timestamp": 1616161616}')
        assert response1.status_code == 200
        response2 = self.client.post("/sign", data='{"timestamp": 1616161616,"message": "Hello World"}')
        assert response2.status_code == 200
        assert response1.json() == response2.json()


    def test_verify_fail(self):
        response = self.client.post("/verify", json={
            "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b26", # wrong signature
            "data": {
                "message": "Hello World",
                "timestamp": 1616161616
            }
        })
        assert response.status_code == 400


    def test_verify_missing_data(self):
        response = self.client.post("/verify", json={
            "signature": "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28"
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Data to verify is required"}


    def test_verify_no_signature(self):
        response = self.client.post("/verify", json={
            "data": {
                "message": "Hello World",
                "timestamp": 1616161616
            }
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Signature is required"}
