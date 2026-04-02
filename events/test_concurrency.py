import pytest
import threading
from django.db import connection
from events.models import Event, Ticket

@pytest.mark.django_db(transaction=True)
def test_double_booking_vulnerability():
    # 1. Arrange: Create an event with ONLY 1 ticket left
    event = Event.objects.create(
        name="The Final Concert",
        total_capacity=100,
        available_tickets=1, # Only one left!
        price=50.00
    )

    # We need a function for the threads to run
    def worker(email):
        # Each thread gets its own database connection
        # and grabs the latest version of the event
        e = Event.objects.get(id=event.id)
        e.buy_ticket_secure(buyer_email=email)
        connection.close()

    # 2. Act: Spin up two separate threads (simulating two rapid requests)
    thread1 = threading.Thread(target=worker, args=("user1@example.com",))
    thread2 = threading.Thread(target=worker, args=("user2@example.com",))

    # Start them at the exact same time
    thread1.start()
    thread2.start()

    # Wait for both to finish
    thread1.join()
    thread2.join()

    # 3. Assert: Refresh the event from the database
    event.refresh_from_db()

    # If the system is secure, we should only have 1 ticket sold, 
    # and available_tickets should be 0.
    
    # Run the test. It might fail these assertions because both threads
    # read available_tickets=1 before either had a chance to save it as 0.
    assert Ticket.objects.count() == 1, "VULNERABILITY: Two tickets were created for one seat!"
    assert event.available_tickets == 0, f"Math is wrong. Tickets left: {event.available_tickets}"