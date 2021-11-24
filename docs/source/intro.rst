.. role:: raw-html-m2r(raw)
   :format: html


Binance Public API Connector Python
===================================


.. image:: https://img.shields.io/badge/python-3.6+-blue.svg
   :target: https://www.python.org/downloads/release/python-360/
   :alt: Python 3.6


.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT


This is a lightweight library that works as a connector to `Binance public API <https://github.com/binance/binance-spot-api-docs>`_.
It's designed to be simple, clean, and easy to use with minimal dependencies.

* Source Code: https://github.com/binance/binance-connector-python
* Official API document:

  * https://github.com/binance/binance-spot-api-docs
  * https://binance-docs.github.io/apidocs/spot/en

* Support channels:

  * Binance developer forum: https://dev.binance.vision/
  * Telegram Channel: https://t.me/binance_api_english

* API key setup: https://www.binance.com/en-NG/support/faq/360002502072
* Testnet API key setup: https://dev.binance.vision/t/99

Features
--------

* Supported APIs:

  * ``/api/*``
  * ``/sapi/*``
  * Spot Websocket Market Stream
  * Spot User Data Stream

* Inclusion of test cases and examples
* Customizable base URL, request timeout and HTTP proxy
* Response metadata can be displayed

Quick Start
-----------

Installation
^^^^^^^^^^^^

* Install via package name

  .. code-block:: bash

     pip install binance-connector

* Alternatively, install with git repository path

  .. code-block:: bash

    python -m pip install git+https://github.com/binance/binance-connector-python.git


Usage
-----

RESTful APIs
^^^^^^^^^^^^

.. code-block:: python

   from binance.spot import Spot 

   client = Spot()
   print(client.time())

   client = Spot(key='<api_key>', secret='<api_secret>')

   # Get account information
   print(client.account())

   # Post a new order
   params = {
       'symbol': 'BTCUSDT',
       'side': 'SELL',
       'type': 'LIMIT',
       'timeInForce': 'GTC',
       'quantity': 0.002,
       'price': 9500
   }

   response = client.new_order(**params)
   print(response)

Please find `examples <https://github.com/binance/binance-connector-python/tree/master/examples>`_ folder to check for more endpoints.


Websocket
^^^^^^^^^

.. code-block:: python

   from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

   def message_handler(message):
       print(message)

   ws_client = WebsocketClient()
   ws_client.start()

   ws_client.mini_ticker(
       symbol='bnbusdt',
       id=1,
       callback=message_handler,
   )

   # Combine selected streams
   ws_client.instant_subscribe(
       stream=['bnbusdt@bookTicker', 'ethusdt@bookTicker'],
       callback=message_handler,
   )

   ws_client.stop()

More websocket examples are available in the `examples <https://github.com/binance/binance-connector-python/tree/master/examples>`_ folder
