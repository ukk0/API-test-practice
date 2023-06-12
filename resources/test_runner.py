from collections import namedtuple
from typing import Any, Dict, List, Optional

from resources.api_client import TestAPI
from resources.request_payloads import (
    create_or_update_booking_payload,
    partial_update_booking_payload,
)

OrderDetails = namedtuple(
    "OrderDetails", ("booking_id", "first_name", "last_name", "check_in", "check_out")
)


class TestRunner:
    def __int__(self, auth_method: str):
        self.auth_method = auth_method
        self.api = TestAPI()

    def create_booking(
        self,
        first_name: Optional[str],
        last_name: Optional[str],
        total_price: Optional[int],
        deposit_paid: Optional[bool],
        check_in: Optional[str],
        check_out: Optional[str],
        additional_needs: Optional[str],
    ) -> OrderDetails:
        payload = create_or_update_booking_payload(
            first_name,
            last_name,
            total_price,
            deposit_paid,
            check_in,
            check_out,
            additional_needs,
        )
        create_booking_response = self.api.create_booking(payload)
        json_response = create_booking_response.json()
        assert create_booking_response.status_code == 200
        assert "bookingid" in json_response
        assert (
            "firstname" in json_response["booking"]
            and json_response["booking"]["firstname"] == payload["firstname"]
        )
        assert (
            "lastname" in json_response["booking"]
            and json_response["booking"]["lastname"] == payload["lastname"]
        )
        assert (
            "totalprice" in json_response["booking"]
            and json_response["booking"]["totalprice"] == payload["totalprice"]
        )
        assert (
            "depositpaid" in json_response["booking"]
            and json_response["booking"]["depositpaid"] == payload["depositpaid"]
        )
        assert (
            "additionalneeds" in json_response["booking"]
            and json_response["booking"]["additionalneeds"]
            == payload["additionalneeds"]
        )
        assert (
            "checkin" in json_response["booking"]["bookingdates"]
            and json_response["booking"]["bookingdates"]["checkin"]
            == payload["bookingdates"]["checkin"]
        )
        assert (
            "checkout" in json_response["booking"]["bookingdates"]
            and json_response["booking"]["bookingdates"]["checkout"]
            == payload["bookingdates"]["checkout"]
        )
        return OrderDetails(
            booking_id=json_response["bookingid"],
            first_name=json_response["firstname"],
            last_name=json_response["lastname"],
            check_in=json_response["check_in"],
            check_out=json_response["checkout"],
        )

    def list_booking_ids(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        check_in: Optional[str] = None,
        check_out: Optional[str] = None,
    ) -> List[Dict[str, int]]:
        booking_id_list = self.api.list_booking_ids(
            first_name, last_name, check_in, check_out
        )
        json_response = booking_id_list.json()
        assert booking_id_list.status_code == 200
        assert isinstance(json_response, list)
        return json_response

    def get_booking_by_id(self, booking_id: str) -> Dict[str, Any]:
        get_booking_response = self.api.get_booking_by_id(booking_id)
        json_response = get_booking_response.json()
        assert get_booking_response.status_code == 200
        assert "firstname" in json_response
        assert "lastname" in json_response
        assert "totalprice" in json_response
        assert "depositpaid" in json_response
        assert "bookingdates" in json_response
        assert "checkin" in json_response["bookingdates"]
        assert "checkout" in json_response["bookingdates"]
        assert "additionalneeds" in json_response
        return json_response
