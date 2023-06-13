import pytest
from resources.test_runner import TestRunner


@pytest.mark.parametrize(
    ("first_name", "last_name"),
    [("Alan", "Shepard"), ("Buzz", "Aldrin"), ("Yuri", "Gagarin")],
)
def test_new_bookings_can_be_created_and_found(first_name, last_name):
    runner = TestRunner()

    # Create bookings with partially set, partially random data
    new_booking = runner.create_booking(first_name=first_name, last_name=last_name)

    # Get the booking by ID
    booking_data = runner.get_booking_by_id(new_booking.booking_id)

    # Compare few fields to validate correct bookings returned
    assert new_booking.first_name == booking_data.first_name
    assert new_booking.last_name == booking_data.last_name
    assert new_booking.total_price == booking_data.total_price
    assert new_booking.additional_needs == booking_data.additional_needs


@pytest.mark.parametrize("auth_method", ["api_key", "cookie_token"])
def test_booking_can_be_deleted_and_both_auth_schemes_are_accepted(auth_method):
    runner = TestRunner(auth_method=auth_method)

    # Create booking with random data
    new_booking_id = runner.create_booking().booking_id

    # Delete booking
    runner.delete_booking(new_booking_id)

    # Check that no booking with this ID no longer exists
    runner.get_booking_by_id(new_booking_id, expect_failure=True)


def test_booking_can_be_fully_updated():
    pass


def test_booking_can_be_partially_updated():
    pass


def test_booking_listing_respects_search_parameters():
    pass
