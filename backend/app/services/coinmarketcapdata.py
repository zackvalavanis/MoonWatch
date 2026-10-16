import json
import os
import ssl
import urllib.parse
import urllib.request

from dotenv import load_dotenv

load_dotenv()

import certifi

CMC_LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
CMC_QUOTES_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
_context = ssl.create_default_context(cafile=certifi.where())


def _cmc_get(url: str, params: dict) -> dict:
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": os.environ["CMC_API_KEY"],
        },
    )
    with urllib.request.urlopen(request, context=_context) as response:
        return json.load(response)


def get_latest_listings(limit: int = 10, convert: str = "USD") -> dict:
    return _cmc_get(CMC_LISTINGS_URL, {"start": 1, "limit": limit, "convert": convert})


def get_coin_by_id(cmc_id: int, convert: str = "USD") -> dict | None:
    try:
        data = _cmc_get(CMC_QUOTES_URL, {"id": cmc_id, "convert": convert})
    except urllib.error.HTTPError as e:
        if e.code == 400:
            return None
        raise
    return data["data"].get(str(cmc_id))


if __name__ == "__main__":
    print(get_coin_by_id(1))
