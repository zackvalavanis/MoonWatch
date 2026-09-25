import json
import os
import ssl
import urllib.parse
import urllib.request

from dotenv import load_dotenv

load_dotenv()

import certifi

CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
_context = ssl.create_default_context(cafile=certifi.where())


def get_latest_listings(limit: int = 10, convert: str = "USD") -> dict:
    params = urllib.parse.urlencode({"start": 1, "limit": limit, "convert": convert})
    request = urllib.request.Request(
        f"{CMC_URL}?{params}",
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": os.environ["CMC_API_KEY"],
        },
    )
    with urllib.request.urlopen(request, context=_context) as response:
        return json.load(response)


if __name__ == "__main__":
    data = get_latest_listings(limit=5)
    for coin in data["data"]:
        print(coin["symbol"], coin["quote"]["USD"]["price"])
