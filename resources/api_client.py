from requests import request, Response
from typing import Optional, Dict, Any, Union
from resources.request_payloads import (
    auth_token_payload,
    create_or_update_booking_payload,
    partial_update_booking_payload,
)

API_URL = "https://restful-booker.herokuapp.com"
API_KEY = "YWRtaW46cGFzc3dvcmQxMjM="  # Hardcoded API value, not a real secret
USER_AGENT = "ukk0-test"
AUTH_METHODS = {"api_key", "cookie_token"}


class TestAPI:
    @classmethod
    def _api_request(
        cls,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
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
            json=auth_token_payload(),
        )
        token = response.json()["token"]
        return token

    @classmethod
    def create_booking(
        cls,
        first_name: str,
        last_name: str,
        total_price: int,
        deposit_paid: bool,
        check_in: str,
        check_out: str,
        additional_needs: Optional[str],
    ) -> Response:
        url = "booking"
        data = create_or_update_booking_payload(
            first_name,
            last_name,
            total_price,
            deposit_paid,
            check_in,
            check_out,
            additional_needs,
        )
        response = cls._api_request(
            url=url, headers=cls._add_headers(), method="POST", json=data
        )
        return response

    @classmethod
    def get_list_of_booking_ids(
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
        first_name: Optional[str],
        last_name: Optional[str],
        total_price: Optional[int],
        deposit_paid: Optional[bool],
        check_in: Optional[str],
        check_out: Optional[str],
        additional_needs: Optional[str],
        partial_update: bool = False,
    ) -> Response:
        url = f"booking/{booking_id}"
        if partial_update:
            data = partial_update_booking_payload(
                first_name,
                last_name,
                total_price,
                deposit_paid,
                check_in,
                check_out,
                additional_needs,
            )
        else:
            data = create_or_update_booking_payload(
                first_name,
                last_name,
                total_price,
                deposit_paid,
                check_in,
                check_out,
                additional_needs,
            )
        method = "PATCH" if partial_update else "PUT"
        response = cls._api_request(
            url=url,
            headers=cls._add_headers(auth_method=auth_method),
            method=method,
            json=data,
        )
        return response

    @classmethod
    def delete_booking(cls, booking_id: str, auth_method: str) -> Response:
        url = f"booking/{booking_id}"
        response = cls._api_request(
            url=url, headers=cls._add_headers(auth_method=auth_method), method="DELETE"
        )
        return response
