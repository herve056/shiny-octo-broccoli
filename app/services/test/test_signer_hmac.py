from ..signer import SignerHMAC


class TestSignerHMAC:

    def setup_class(self):
        self.signer = SignerHMAC("default-secret-key".encode())

    def test_json_signature(self):
        assert self.signer.sign({"message": "Hello World", "timestamp": 1616161616}) == \
            "6f86ed04940841c6c5f1690c1ec957869a1daf72b73eba63ff9bec98c5158b28"
