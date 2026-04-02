from rest_framework import serializers
from .models import Event, Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'buyer_email', 'purchased_at']

class EventSerializer(serializers.ModelSerializer):
    # This is where the N+1 trap is set. We are asking DRF to also 
    # fetch all the tickets associated with this event.
    tickets = TicketSerializer(many=True, read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'total_capacity', 'available_tickets', 'price', 'is_sold_out', 'tickets']