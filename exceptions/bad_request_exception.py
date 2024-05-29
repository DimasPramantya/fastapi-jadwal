from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class BadRequestException(HTTPException):
    def __init__(self, message: str):
        detail = message
        super().__init__(status_code=400, detail=detail)


async def badRequestExceptionHandler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )