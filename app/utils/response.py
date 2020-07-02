from fastapi.responses import UJSONResponse


class GeneralResponse(UJSONResponse):
    __slots__ = []

    def __init__(self, result, code=200, message=None):
        content = {'result': result}
        if message:
            content.update({'message': message})
        super().__init__(status_code=code, content=content)
