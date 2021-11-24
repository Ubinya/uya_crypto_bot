import responses

from tests.util import random_str
from tests.util import mock_http_response
from binance.spot import Spot as Client

mock_item = {"key_1": "value_1", "key_2": "value_2"}

key = random_str()
secret = random_str()


@mock_http_response(
    responses.GET, "/sapi/v1/lending/daily/product/list", mock_item, 200
)
def test_savings_flexible_products():
    """Tests the API endpoint to get flexible product list"""

    client = Client(key, secret)
    response = client.savings_flexible_products()
    response.should.equal(mock_item)
