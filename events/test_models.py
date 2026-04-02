import pytest
from events.models import Event

# This decorator tells pytest to give this test access to the database
@pytest.mark.django_db
def test_create_event_initializes_correctly():

    event = Event.objects.create(  
        name = "Tech Conference 2026",
        total_capacity=500,
        available_tickets=500,              
        price=150.00
    )
    # Now we check if the event was created with the correct values with assert
    assert event.name == "Tech Conference 2026"
    assert event.total_capacity == 500
    assert event.available_tickets == 500
    assert event.is_sold_out is False