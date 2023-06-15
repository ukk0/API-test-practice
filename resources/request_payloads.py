from random import choice, randint
from typing import Any, Dict

from lorem_text import lorem


def create_or_update_booking_payload(
    first_name: str,
    last_name: str,
    total_price: int,
    deposit_paid: bool,
    check_in: str,
    check_out: str,
    additional_needs: str,
) -> Dict[str, Any]:
    payload = {
        "firstname": first_name or lorem.words(1),
        "lastname": last_name or lorem.words(1),
        "totalprice": total_price or randint(100, 1000),
        "depositpaid": deposit_paid or False,
        "bookingdates": {
            "checkin": check_in or "1970-01-01",
            "checkout": check_out or "2038-01-19",
        },
        "additionalneeds": additional_needs or lorem.words(5),
    }
    return payload


def partial_update_booking_payload(
    first_name: str,
    last_name: str,
    total_price: int,
    deposit_paid: bool,
    check_in: str,
    check_out: str,
    additional_needs: str,
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
