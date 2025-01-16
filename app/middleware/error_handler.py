#app/middleware/error_handler.py

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Union

async def error_handler(request: Request, call_next) -> Union[Response, JSONResponse]:
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "path": request.url.path
            }
        )
