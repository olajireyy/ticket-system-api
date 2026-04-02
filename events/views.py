from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import Event
from .serializers import EventSerializer
from rest_framework.throttling import ScopedRateThrottle

class EventListView(APIView):
    serializer_class = EventSerializer

    def get(self, request):
        #Check if the data is already in Redis
        cache_key = 'all_events_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            # FAST PATH: Return directly from Redis memory. PostgreSQL does nothing.
            print("CACHE HIT: Served from Redis")
            return Response(cached_data, status=status.HTTP_200_OK)
        
        #SLOW PATH: Data wasn't in Redis. We must hit PostgreSQL.
        print("CACHE MISS: Hitting PostgreSQL")
        events = Event.objects.prefetch_related('tickets').all()
        serializer = EventSerializer(events, many=True)

        # Store the result in Redis for future requests
        cache.set(cache_key, serializer.data, timeout=300)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyTicketView(APIView):
    # Apply the strict rate limit to this specific view
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'purchase'

    def post(self, request, event_id):
        buyer_email = request.data.get('email')
        
        if not buyer_email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        success = event.buy_ticket_secure(buyer_email)

        if success:
            return Response({"message": "Ticket purchased successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Event is sold out!"}, status=status.HTTP_409_CONFLICT)