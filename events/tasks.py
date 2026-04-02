from celery import shared_task
import time

@shared_task
def send_ticket_email(buyer_email, event_name):
 
    print(f"Starting to generate PDF and send email to {buyer_email}...")
    
    # Simulate a slow 5-second process
    time.sleep(5) 
    
    print(f"SUCCESS: Email sent to {buyer_email} for {event_name}!")
    return True