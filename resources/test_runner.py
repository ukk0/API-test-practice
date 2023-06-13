from collections import namedtuple
from typing import Dict, List, Optional, Union
from requests import Response

from resources.api_client import TestAPI
from resources.request_payloads import (
    create_or_update_booking_payload,
    partial_update_booking_payload,
)

OrderDetails = namedtuple(
    "OrderDetails",
    (
        "booking_id",
        "first_name",
        "last_name",
        "total_price",
        "deposit_paid",
        "check_in",
        "check_out",
        "additional_needs",
    ),
)


class TestRunner:
    def __init__(self, auth_method: Optional[str] = None):
        self.auth_method = auth_method
        self.api = TestAPI()

    def create_booking(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        total_price: Optional[int] = None,
        deposit_paid: Optional[bool] = None,
        check_in: Optional[str] = None,
        check_out: Optional[str] = None,
        additional_needs: Optional[str] = None,
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
            first_name=json_response["booking"]["firstname"],
            last_name=json_response["booking"]["lastname"],
            total_price=json_response["booking"]["totalprice"],
            deposit_paid=json_response["booking"]["depositpaid"],
            check_in=json_response["booking"]["bookingdates"]["checkin"],
            check_out=json_response["booking"]["bookingdates"]["checkout"],
            additional_needs=json_response["booking"]["additionalneeds"],
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

    def get_booking_by_id(
        self, booking_id: str, expect_failure: bool = False
    ) -> Union[OrderDetails, Response]:
        get_booking_response = self.api.get_booking_by_id(booking_id)
        if expect_failure:
            assert get_booking_response.status_code == 404
            return get_booking_response
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

        return OrderDetails(
            booking_id=booking_id,
            first_name=json_response["firstname"],
            last_name=json_response["lastname"],
            total_price=json_response["totalprice"],
            deposit_paid=json_response["depositpaid"],
            check_in=json_response["bookingdates"]["checkin"],
            check_out=json_response["bookingdates"]["checkout"],
            additional_needs=json_response["additionalneeds"],
        )

    def update_booking(
        self,
        booking_id: str,
        partial_update: bool = False,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        total_price: Optional[int] = None,
        deposit_paid: Optional[bool] = None,
        check_in: Optional[str] = None,
        check_out: Optional[str] = None,
        additional_needs: Optional[str] = None,
    ) -> OrderDetails:
        payload = (
            partial_update_booking_payload(
                first_name,
                last_name,
                total_price,
                deposit_paid,
                check_in,
                check_out,
                additional_needs,
            )
            if partial_update
            else create_or_update_booking_payload(
                first_name,
                last_name,
                total_price,
                deposit_paid,
                check_in,
                check_out,
                additional_needs,
            )
        )
        update_booking_response = self.api.update_booking(
            booking_id, self.auth_method, payload, partial_update
        )
        json_response = update_booking_response.json()
        assert update_booking_response.status_code == 200
        assert "firstname" in json_response
        assert "lastname" in json_response
        assert "totalprice" in json_response
        assert "depositpaid" in json_response
        assert "additionalneeds" in json_response
        assert "checkin" in json_response["bookingdates"]
        assert "checkout" in json_response["bookingdates"]
        if first_name:
            assert first_name == json_response["firstname"]
        if last_name:
            assert last_name == json_response["lastname"]
        if total_price:
            assert total_price == json_response["totalprice"]
        if deposit_paid:
            assert deposit_paid == json_response["depositpaid"]
        if additional_needs:
            assert additional_needs == json_response["additionalneeds"]
        if check_in:
            assert check_in == json_response["bookingdates"]["checkin"]
        if check_out:
            assert check_in == json_response["bookingdates"]["checkout"]

        return OrderDetails(
            booking_id=booking_id,
            first_name=json_response["firstname"],
            last_name=json_response["lastname"],
            total_price=json_response["totalprice"],
            deposit_paid=json_response["depositpaid"],
            check_in=json_response["bookingdates"]["checkin"],
            check_out=json_response["bookingdates"]["checkout"],
            additional_needs=json_response["additionalneeds"],
        )

    def delete_booking(self, booking_id: str):
        delete_booking_response = self.api.delete_booking(booking_id, self.auth_method)
        assert delete_booking_response.status_code == 201
