import asyncio as aio

from starlette.applications import Starlette as VanillaStarlette
from starlette.endpoints import HTTPEndpoint as StarletteHTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.routing import Route

try:
    import ujson  # noqa
    from starlette.responses import UJSONResponse as JSONResponse  # noqa
except ImportError:
    pass


__version__ = "0.0.4"
__license__ = "MIT"


async def result_to_response(result):
    """Convert an result to Starlette Response."""

    while aio.iscoroutine(result):
        result = await result

    if isinstance(result, Response):
        return result

    if isinstance(result, (str, bytes)):
        return HTMLResponse(result)

    if isinstance(result, tuple):
        status, *result = result
        response = await result_to_response(*result)
        response.status_code = status
        return response

    return JSONResponse(result)


def endpoint_to_asgi(endpoint):
    """Create an app from an endpoint."""

    async def app(scope, receive, send):
        """Process an endpoint result."""

        request = Request(scope, receive=receive, send=send)
        result = endpoint(request)
        response = await result_to_response(result)
        return await response(scope, receive, send)

    return app


def patch_routes(app):

    def handler():
        """Patch routes when the app starts."""
        for route in app.routes:
            if isinstance(route, Route) and route.app is not route.endpoint:
                route.app = endpoint_to_asgi(route.endpoint)

    return handler


def Views(app: VanillaStarlette) -> VanillaStarlette:
    """Patch Starlette Application."""

    if isinstance(app, VanillaStarlette) and not isinstance(app, Starlette):
        app.router.on_startup.append(patch_routes(app))

    return app


class Starlette(VanillaStarlette):

    def __init__(self, *args, on_startup=None, **kwargs):
        on_startup = on_startup or []
        on_startup.append(patch_routes(self))
        super().__init__(*args, on_startup=on_startup, **kwargs)


class HTTPEndpoint(StarletteHTTPEndpoint):

    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        handler_name = "get" if request.method == "HEAD" else request.method.lower()
        handler = getattr(self, handler_name, self.method_not_allowed)
        result = handler(request)
        response = await result_to_response(result)
        await response(self.scope, self.receive, self.send)
