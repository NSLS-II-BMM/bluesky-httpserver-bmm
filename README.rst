======================
bluesky-httpserver-bmm
======================

.. image:: https://img.shields.io/travis/dmgav/bluesky-httpserver-bmm.svg
        :target: https://travis-ci.org/dmgav/bluesky-httpserver-bmm

.. image:: https://img.shields.io/pypi/v/bluesky-httpserver-bmm.svg
        :target: https://pypi.python.org/pypi/bluesky-httpserver-bmm


Bluesky HTTP Server: custom processing modules for BMM beamline.

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://dmgav.github.io/bluesky-httpserver-bmm.

Features
--------

The repository contains modules with custom request processing code for Bluesky HTTP Server.

Install the package in the desired conda environment as::

  pip install .

For develop installation use::

  pip install -e .

Start Bluesky HTTP Server as::

  BLUESKY_HTTPSERVER_CUSTOM_MODULE=bluesky-httpserver-bmm uvicorn bluesky_queueserver.server.server:app --host localhost --port 60610

or set the environment variable **BLUESKY_HTTPSERVER_CUSTOM_MODULE** before starting the server::

  export BLUESKY_HTTPSERVER_CUSTOM_MODULE=bluesky-httpserver-bmm
  uvicorn bluesky_queueserver.server.server:app --host localhost --port 60610

Included custom functions:

- **spreadsheet_to_plan_list"** for *.xlsx*, *.xlsm*, *.xltx* and *.xltm* files. Supports
**data_type** = *wheel_xafs*.
