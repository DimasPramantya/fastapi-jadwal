from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class EntityNotFoundException(HTTPException):
    def __init__(self, entity_name: str, entity_id: int):
        detail = f"{entity_name} with id {entity_id} not found"
        super().__init__(status_code=404, detail=detail)


async def entityNotFoundExceptionHandler(request: Request, exc: EntityNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )