from django.urls import path
from .views import EventListView, BuyTicketView

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:event_id>/buy/', BuyTicketView.as_view(), name='buy-ticket'),
]