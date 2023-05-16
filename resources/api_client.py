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

    @staticmethod
    def _add_headers(
        api_key: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if api_key:
            headers.update({"Authorization": f"Basic {api_key}"})
        if token:
            headers.update({"Cookie": f"token={token}"})
        return headers

    @classmethod
    def create_auth_token(cls) -> str:
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
        additional_needs: Optional[str] = None,
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
        response = cls._api_request(url=url, headers=cls._add_headers(), method="POST", json=data)
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
    def get_booking_by_id(cls) -> Response:
        pass

    @classmethod
    def update_booking(cls) -> Response:
        pass

    @classmethod
    def partial_update_booking(cls) -> Response:
        pass

    @classmethod
    def delete_booking(cls) -> Response:
        pass

