Starlette-Views
###############

.. _description:

**starlette-views** -- A helper to make views faster with Starlette_

Starlette-Views automatically converts views results into
`starlette.responses.Response` objects.

.. _badges:

.. image:: https://github.com/klen/starlette-views/workflows/tests/badge.svg
    :target: https://github.com/klen/starlette-views/actions
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/starlette-views
    :target: https://pypi.org/project/starlette-views/
    :alt: PYPI Version

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 3.7

.. _installation:

Installation
=============

**starlette-views** should be installed using pip: ::

    pip install starlette-views


Initialization
==============

Just wrap your `Starlette` application into the views:

.. code:: python

   from starlette_views import Views

   app = Starlette(...)
   app = Views(app)


or you are able to import `Starlette` from the module (in this case you have
nothing to setup more):

.. code:: python

   from starlette_views import Starlette

   app = Starlette(...)


.. _usage:

Quick Start
===========

.. code:: python

   from starlette.applications import Starlette
   from starlette.routing import Route


   async def hello(request):
       return 'Hello from Views!'

    # Create Starlette Application
   app = Starlette(routes=[
        Route('/', hello)
   ])

   # Enable the quick views
   app = Views(app)


Then run the application...

.. code::

   $ uvicorn example:app


Open http://127.0.0.1:8000 and you will find the hello from the views.


Usage
=====

.. code:: python

    async def render_json1(request):
        """Just return dictionary to make a JSON response."""
        return {'any': 'value'}


    async def render_json2(request):
        """List also works well."""
        return [{'any': 'value'}]


    async def render_json3(request):
        """Return a tuple to set HTTP status."""
        return 403, {'message': 'Authorization required'}


    async def render_html1(request):
        """Return any string to make an HTML response."""
        return "<h1>I would be rendered as HTML</h1>"


    async def render_html2(request):
        """Return a tuple to set HTTP status."""
        return 201, 'Record Created'


    # Starlette Responses works as well too
    from starlette.responses import HTMLResponse


    async def render_normal(request):
        """Starlette Responses are returned as is."""
        return HTMLResponse('Common behaviour', status_code=200)


.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/starlette-views/issues

.. _contributing:

Contributing
============

Development of the project happens at: https://github.com/klen/starlette-views

.. _license:

License
========

Licensed under a `MIT license`_.


.. _links:

.. _klen: https://github.com/klen
.. _MIT license: http://opensource.org/licenses/MIT
.. _Starlette: https://starlette.io

