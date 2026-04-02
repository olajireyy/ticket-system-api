from django.core.cache import cache
from django.db import models, transaction
from .tasks import send_ticket_email
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    total_capacity = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def is_sold_out(self):
        return self.available_tickets <= 0
    
    def __str__(self):
        return self.name

    def buy_ticket_secure(self, buyer_email):
 
        with transaction.atomic():
            locked_event = Event.objects.select_for_update().get(id=self.id)

            if locked_event.available_tickets > 0:
                Ticket.objects.create(event=locked_event, buyer_email=buyer_email)
                locked_event.available_tickets -= 1
                locked_event.save()
                #cache destroy stale data in Redis. Next request will trigger a cache miss and fetch fresh data from PostgreSQL.
                cache.delete('all_events_list')
                #celery
                send_ticket_email.delay(buyer_email, locked_event.name)
                return True
            return False
        
        
class Ticket(models.Model):
    # The ForeignKey ties this ticket to a specific event. 
    # 'related_name' allows us to do event.tickets.all()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    buyer_email = models.EmailField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} - {self.buyer_email}"