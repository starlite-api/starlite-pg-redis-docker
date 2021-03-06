import logging

from starlette.responses import Response
from starlite.middleware import ExceptionHandlerMiddleware
from starlite.types import Request

logger = logging.getLogger(__name__)


def logging_exception_handler(request: Request, exc: Exception) -> Response:
    """
    Logs exception and returns appropriate response.

    Parameters
    ----------
    request : Request
        The request that caused the exception.
    exc :
        The exception caught by the Starlite exception handling middleware and passed to the
        callback.

    Returns
    -------
    Response
    """
    logger.error("Application Exception", exc_info=exc)
    return ExceptionHandlerMiddleware(
        app=request.app, debug=request.app.debug, exception_handlers={}
    ).default_http_exception_handler(request, exc)
