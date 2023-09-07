import pytest
from resources.test_runner import TestRunner


@pytest.mark.parametrize(
    ("first_name", "last_name"),
    [("Alan", "Shepard"), ("Yuri", "Gagarin")],
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


@pytest.mark.parametrize("auth_method", ["api_key", "cookie_token", "invalid_auth"])
def test_deletion_with_auth_schemes_respected(auth_method):
    runner = TestRunner(auth_method=auth_method)

    # Create booking with random data
    new_booking_id = runner.create_booking().booking_id

    # Delete booking
    try:
        runner.delete_booking(new_booking_id)
    except ValueError:
        if auth_method == "invalid_auth":
            assert True

    # Check that no booking with this ID no longer exists
    runner.get_booking_by_id(
        new_booking_id, expect_failure=True if auth_method != "invalid_auth" else False
    )


def test_booking_can_be_fully_updated():
    runner = TestRunner(auth_method="api_key")

    # Create booking with random data
    new_booking_data = runner.create_booking()
    booking_id = new_booking_data.booking_id

    # Update booking with all new data
    update_data = runner.update_booking(
        booking_id=booking_id,
        first_name="Testy",
        last_name="McTester",
        total_price=2000,
        deposit_paid=True,
        check_in="2020-01-01",
        check_out="2020-01-10",
        additional_needs="Breakfast",
    )

    # Get booking data and check it was updated
    attributes_to_compare = [
        "first_name",
        "last_name",
        "total_price",
        "deposit_paid",
        "check_in",
        "check_out",
        "additional_needs",
    ]

    current_data = runner.get_booking_by_id(booking_id=booking_id)
    for attr in attributes_to_compare:
        assert (
            getattr(update_data, attr)
            == getattr(current_data, attr)
            != getattr(new_booking_data, attr)
        )


def test_booking_can_be_partially_updated():
    runner = TestRunner(auth_method="api_key")

    # Create booking with random data
    new_booking_data = runner.create_booking()
    booking_id = new_booking_data.booking_id

    # Update name fields and validate they have been changed
    update_data = runner.update_booking(
        booking_id=booking_id,
        partial_update=True,
        first_name="Testy",
        last_name="McTester",
    )
    assert new_booking_data.first_name != update_data.first_name
    assert new_booking_data.last_name != update_data.last_name

    # Update price and deposit fields and validate they have been changed
    update_data = runner.update_booking(
        booking_id=booking_id,
        partial_update=True,
        total_price=2000,
        deposit_paid=True,
    )
    assert new_booking_data.total_price != update_data.total_price
    assert new_booking_data.deposit_paid != update_data.deposit_paid

    # Update checkin and checkout fields and validate they have been changed
    update_data = runner.update_booking(
        booking_id=booking_id,
        partial_update=True,
        check_in="2020-01-01",
        check_out="2020-01-10",
    )
    assert new_booking_data.check_in != update_data.check_in
    assert new_booking_data.check_out != update_data.check_out


def test_booking_listing_respects_search_parameters():
    runner = TestRunner(auth_method="api_key")

    # Search for bookings with certain parameters
    list_of_bookings = runner.list_booking_ids(first_name="Testy", last_name="McTester")

    # Validate returned bookings match the search parameters
    for booking in list_of_bookings:
        booking_data = runner.get_booking_by_id(booking_id=str(booking["bookingid"]))
        assert booking_data.first_name == "Testy"
        assert booking_data.last_name == "McTester"


# test comment