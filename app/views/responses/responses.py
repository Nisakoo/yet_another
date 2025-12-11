from typing import Union

from django.http import JsonResponse


# Стоит ли все переписать с typing?
class BaseResponse(JsonResponse):
    def __init__(self, *, status: str, status_code: int, message: Union[str | None] = None, data: Union[dict | None] = None, **kwargs):
        payload = {
            "status": status,
            "message": message,
        }

        if data:
            payload.update(data)

        super().__init__(
            payload,
            status=status_code,
            **kwargs
        )


class OkResponse(BaseResponse):
    def __init__(self, *, status_code: int, message: Union[str | None] = None, data: Union[dict | None] = None, **kwargs):
        super().__init__(
            status="ok",
            status_code=status_code,
            message=message,
            data=data,
            **kwargs
        )


class ErrorResponse(BaseResponse):
    def __init__(self, *, status_code: int, message: Union[str | None] = None, data: Union[dict | None] = None, **kwargs):
        super().__init__(
            status="error",
            status_code=status_code,
            message=message,
            data=data,
            **kwargs
        )