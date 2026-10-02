from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

import requests


class BitFlyerClient:
    BASE_URL = "https://api.bitflyer.com"

    def __init__(self, api_key: str = "", api_secret: str = "", timeout: float = 10.0):
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.session = requests.Session()

    def _public_get(self, path: str, params: dict[str, Any] | None = None):
        response = self.session.get(
            self.BASE_URL + path,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def _private_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ):
        if not self.api_key or not self.api_secret:
            raise RuntimeError("Private API requires BITFLYER_API_KEY and BITFLYER_API_SECRET")

        method = method.upper()
        query = ""
        if params:
            query = "?" + urlencode(params)

        body_text = ""
        if body is not None:
            body_text = json.dumps(body, separators=(",", ":"))

        timestamp = str(time.time())
        signing_path = path + query
        text = timestamp + method + signing_path + body_text
        sign = hmac.new(
            self.api_secret.encode("utf-8"),
            text.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-SIGN": sign,
            "Content-Type": "application/json",
        }

        response = self.session.request(
            method,
            self.BASE_URL + signing_path,
            data=body_text if body is not None else None,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        if not response.text:
            return None
        return response.json()

    def ticker(self, product_code: str):
        return self._public_get("/v1/ticker", {"product_code": product_code})

    def board(self, product_code: str):
        return self._public_get("/v1/getboard", {"product_code": product_code})

    def markets(self):
        return self._public_get("/v1/getmarkets")

    def permissions(self):
        return self._private_request("GET", "/v1/me/getpermissions")

    def balance(self):
        return self._private_request("GET", "/v1/me/getbalance")

    def trading_commission(self, product_code: str) -> float:
        data = self._private_request(
            "GET",
            "/v1/me/gettradingcommission",
            params={"product_code": product_code},
        )
        return float(data["commission_rate"])

    def child_orders(self, product_code: str, state: str | None = None):
        params = {"product_code": product_code}
        if state:
            params["child_order_state"] = state
        return self._private_request("GET", "/v1/me/getchildorders", params=params)

    def executions(self, product_code: str, count: int = 100):
        return self._private_request(
            "GET",
            "/v1/me/getexecutions",
            params={"product_code": product_code, "count": count},
        )

    def send_limit_order(
        self,
        product_code: str,
        side: str,
        price: int,
        size: float,
        time_in_force: str = "GTC",
    ):
        body = {
            "product_code": product_code,
            "child_order_type": "LIMIT",
            "side": side,
            "price": int(price),
            "size": float(size),
            "time_in_force": time_in_force,
        }
        return self._private_request("POST", "/v1/me/sendchildorder", body=body)
