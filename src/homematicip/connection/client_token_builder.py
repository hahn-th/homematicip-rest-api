import hashlib


class ClientTokenBuilder:

    @staticmethod
    def build_client_token(accesspoint_id: str):
        return (
            hashlib.sha512(str(accesspoint_id + "jiLpVitHvWnIGD1yo7MA").encode("utf-8"))
            .hexdigest()
            .upper()
        )
