import json


class FakeResponse:
    def __init__(self, status=200, body={}, content_type="application/json"):
        self.status = status
        self.body = body
        self.content_type = content_type

    async def json(self):
        return json.dumps(self.body)

    async def release(self):
        pass


def mockreturn(
    return_status=None, return_body={}, content_type="application/json", exception=None
):
    async def mocked(path, data, headers):
        if exception:
            raise exception
        else:
            return FakeResponse(
                status=return_status, body=return_body, content_type=content_type
            )

    return mocked
