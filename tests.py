import pytest


from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_views import Views, HTTPEndpoint


@pytest.fixture(scope='session')
def app():
    return Views(Starlette())


def test_initialization():
    from starlette_views import Starlette  # noqa

    app = Starlette(routes=[
        Route('/hello', lambda r: 'Hello from Views!'),
    ])

    with TestClient(app) as client:
        res = client.get('/hello')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'text/html; charset=utf-8'
        assert res.text == 'Hello from Views!'


def test_endpoint(app):

    class Endpoint(HTTPEndpoint):

        async def get(self, request):
            return 'Hello from an endpoint!'

    app.add_route('/endpoint', Endpoint)

    with TestClient(app) as client:
        res = client.get('/endpoint')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'text/html; charset=utf-8'
        assert res.text == 'Hello from an endpoint!'


def test_status(app):

    @app.route('/404')
    async def page404(request):
        return 404, 'Not Found'

    with TestClient(app) as client:
        res = client.get('/404')
        assert res.status_code == 404
        assert res.headers['content-type'] == 'text/html; charset=utf-8'
        assert res.text == 'Not Found'


def test_html(app):

    @app.route('/html')
    async def html(request):
        return 'HTML CONTENT'

    with TestClient(app) as client:
        res = client.get('/html')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'text/html; charset=utf-8'
        assert res.text == 'HTML CONTENT'


def test_json(app):

    @app.route('/json1')
    async def json1(request):
        return {'json': True}

    with TestClient(app) as client:
        res = client.get('/json1')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'application/json'
        assert res.json() == {'json': True}

    @app.route('/json2')
    async def json2(request):
        return [{'json': True}]

    with TestClient(app) as client:
        res = client.get('/json2')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'application/json'
        assert res.json() == [{'json': True}]

    @app.route('/json3')
    async def json2(request):
        return 403, [{'json': True}]

    with TestClient(app) as client:
        res = client.get('/json3')
        assert res.status_code == 403
        assert res.headers['content-type'] == 'application/json'
        assert res.json() == [{'json': True}]

    @app.route('/none')
    async def none(request):
        return

    with TestClient(app) as client:
        res = client.get('/none')
        assert res.status_code == 200
        assert res.headers['content-type'] == 'application/json'
        assert res.json() is None


def test_response(app):

    @app.route('/response')
    async def response(request):
        return Response('RESPONSE', status_code=201, media_type='text/plain')

    with TestClient(app) as client:
        res = client.get('/response')
        assert res.status_code == 201
        assert res.text == 'RESPONSE'


# pylama:ignore=E402
