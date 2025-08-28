from .encoder import EncoderBase64


class TestEncoderBase64:

    def setup_class(self):
        self.encoder = EncoderBase64()

    def test_encode_values(self):
        # String
        assert self.encoder.encode("Hello, World!") == "SGVsbG8sIFdvcmxkIQ==" # Hello, World!
        # Numbers
        assert self.encoder.encode(123) == "MTIz" # 123
        assert self.encoder.encode(-3.14) == "LTMuMTQ=" # -3.14
        # Booleans
        assert self.encoder.encode(True) == "dHJ1ZQ==" # true
        assert self.encoder.encode(False) == "ZmFsc2U=" # false
        # Null
        assert self.encoder.encode(None) == "bnVsbA==" # null
        # Json Array
        assert self.encoder.encode([1, 2, 3]) == "WzEsMiwzXQ==" # [1,2,3]
        # Json Object
        assert self.encoder.encode({"key": "value"}) == "eyJrZXkiOiJ2YWx1ZSJ9" # {"key":"value"}

    def test_decode_values(self):
        # String
        assert self.encoder.decode("SGVsbG8sIFdvcmxkIQ==") == "Hello, World!"
        # Numbers
        assert self.encoder.decode("MTIz") == 123
        assert self.encoder.decode("LTMuMTQ=") == -3.14
        # Booleans
        assert self.encoder.decode("dHJ1ZQ==") == True
        assert self.encoder.decode("ZmFsc2U=") == False
        # Null
        assert self.encoder.decode("bnVsbA==") == None
        # Json Array
        assert self.encoder.decode("WzEsMiwzXQ==") == [1, 2, 3]
        # Json Object
        assert self.encoder.decode("eyJrZXkiOiJ2YWx1ZSJ9") == {"key": "value"}

    def test_decode_non_encoded_string(self):
        assert self.encoder.decode("not encoded string") == "not encoded string"
    
    def test_decode_special_chars(self):
        assert self.encoder.decode(self.encoder.encode("🥲")) == "🥲"
        assert self.encoder.decode(self.encoder.encode("©")) == "©"
        assert self.encoder.decode(self.encoder.encode("你好")) == "你好"
