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

  QSERVER_CUSTOM_MODULE=bluesky-httpserver-bmm uvicorn bluesky_queueserver.server.server:app --host localhost --port 60610

or set the environment variable **BLUESKY_HTTPSERVER_CUSTOM_MODULE** before starting the server::

  export QSERVER_CUSTOM_MODULE=bluesky-httpserver-bmm
  uvicorn bluesky_queueserver.server.server:app --host localhost --port 60610

Included custom functions:

- **spreadsheet_to_plan_list"** for *.xlsx*, *.xlsm*, *.xltx* and *.xltm* files. Supports
**data_type** = *wheel_xafs*.

Running the Queue Server in the testing environment
---------------------------------------------------

Install *httpie* (*http* command): https://httpie.org/docs#installation

The test will require 3 shells to be opened. In each shell set the current directory::

  cd <path-to-the-repository-root>/bluesky_httpserver_bmm/tests/data

Start Queue Server in shell #1::

  start-re-manager --startup-dir ./simulated_startup_dir

Start HTTP server in shell #2 as instructed above.

Run the following command in shell #3 to upload the spreadsheet::

  http --form POST http://localhost:60610/queue/upload/spreadsheet spreadsheet@sample_ss_wheel_xafs_1.xlsx data_type=wheel_xafs
