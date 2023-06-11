from typing import Optional, Dict, Any


def auth_token_payload() -> Dict[str, str]:  # Hardcoded API values, not real secrets
    payload = {"username": "admin", "password": "password123"}
    return payload


def create_or_update_booking_payload(
    first_name: Optional[str] = "FIRST",
    last_name: Optional[str] = "LAST",
    total_price: Optional[int] = 150,
    deposit_paid: Optional[bool] = False,
    check_in: Optional[str] = "1970-01-01",
    check_out: Optional[str] = "2038-01-19",
    additional_needs: Optional[str] = None,
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
    first_name: Optional[str],
    last_name: Optional[str],
    total_price: Optional[int],
    deposit_paid: Optional[bool],
    check_in: Optional[str],
    check_out: Optional[str],
    additional_needs: Optional[str],
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
