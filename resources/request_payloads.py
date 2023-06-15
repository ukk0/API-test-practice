from random import choice, randint
from typing import Any, Dict, Optional

from lorem_text import lorem


def create_or_update_booking_payload(
    first_name: Optional[str] = lorem.words(1),
    last_name: Optional[str] = lorem.words(1),
    total_price: Optional[int] = randint(100, 1000),
    deposit_paid: Optional[bool] = choice([True, False]),
    check_in: Optional[str] = "1970-01-01",
    check_out: Optional[str] = "2038-01-19",
    additional_needs: Optional[str] = lorem.words(5),
) -> Dict[str, Any]:
    payload = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": total_price,
        "depositpaid": deposit_paid,
        "bookingdates": {
            "checkin": check_in,
            "checkout": check_out,
        },
        "additionalneeds": additional_needs,
    }
    return payload


def partial_update_booking_payload(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    total_price: Optional[int] = None,
    deposit_paid: Optional[bool] = None,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None,
    additional_needs: Optional[str] = None,
) -> Dict[str, Any]:
    payload = {}
    if first_name:
        payload.update({"firstname": first_name})
    if last_name:
        payload.update({"lastname": last_name})
    if total_price:
        payload.update({"totalprice": total_price})
    if deposit_paid:
        payload.update({"depositpaid": deposit_paid})
    if check_in:
        payload.update({"bookingdates": {"checkin": check_in}})
    if check_out:
        payload.update({"bookingdates": {"checkout": check_out}})
    if additional_needs:
        payload.update({"additionalneeds": additional_needs})
    return payload
