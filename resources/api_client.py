from typing import Any, Dict, Optional, Union
from requests import Response, request

API_URL = "https://restful-booker.herokuapp.com"
API_KEY = "YWRtaW46cGFzc3dvcmQxMjM="  # Hardcoded API value, not a real secret
USER_AGENT = "Automatic-API-test"
AUTH_METHODS = {"api_key", "cookie_token"}


class TestAPI:
    @classmethod
    def _api_request(
        cls,
        url: str,
        headers: Dict[str, Any],
        method: str = "GET",
        timeout: int = 100,
        json: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Union[Dict[str, Any], Response]:
        url = f"{API_URL}/{url}"
        return request(
            method=method,
            url=url,
            timeout=timeout,
            headers=headers,
            json=json,
            **kwargs,
        )

    @classmethod
    def _add_headers(cls, auth_method: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if auth_method is not None and auth_method not in AUTH_METHODS:
            raise ValueError(f"Authorization method must be one of {AUTH_METHODS}")
        elif auth_method == "api_key":
            headers.update({"Authorization": f"Basic {API_KEY}"})
        elif auth_method == "cookie_token":
            headers.update({"Cookie": f"token={cls._get_auth_token()}"})
        return headers

    @classmethod
    def _get_auth_token(cls) -> str:
        url = "auth"
        response = cls._api_request(
            url=url,
            headers=cls._add_headers(),
            method="POST",
            json=cls._auth_token_payload(),
        )
        token = response.json()["token"]
        return token

    @staticmethod
    def _auth_token_payload() -> Dict[str, str]:  # not real secrets
        return {"username": "admin", "password": "password123"}

    @classmethod
    def create_booking(cls, request_payload: Dict[str, Any]) -> Response:
        url = "booking"
        response = cls._api_request(
            url=url, headers=cls._add_headers(), method="POST", json=request_payload
        )
        return response

    @classmethod
    def list_booking_ids(
        cls,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        check_in: Optional[str] = None,
        check_out: Optional[str] = None,
    ) -> Response:
        url = "booking"
        query_params = []
        if first_name:
            query_params.append(f"firstname={first_name}")
        if last_name:
            query_params.append(f"lastname={last_name}")
        if check_in:
            query_params.append(f"checkin={check_in}")
        if check_out:
            query_params.append(f"checkout={check_out}")
        if query_params:
            url += "?" + "&".join(query_params)

        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

    @classmethod
    def get_booking_by_id(cls, booking_id: str) -> Response:
        url = f"booking/{booking_id}"
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

    @classmethod
    def update_booking(
        cls,
        booking_id: str,
        auth_method: str,
        request_payload: Dict[str, Any],
        partial_update: bool = False,
    ) -> Response:
        url = f"booking/{booking_id}"
        method = "PATCH" if partial_update else "PUT"
        response = cls._api_request(
            url=url,
            headers=cls._add_headers(auth_method=auth_method),
            method=method,
            json=request_payload,
        )
        return response

    @classmethod
    def delete_booking(cls, booking_id: str, auth_method: str) -> Response:
        url = f"booking/{booking_id}"
        response = cls._api_request(
            url=url, headers=cls._add_headers(auth_method=auth_method), method="DELETE"
        )
        return response

    @classmethod
    def ping_api(cls) -> Response:
        url = "ping"
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response
