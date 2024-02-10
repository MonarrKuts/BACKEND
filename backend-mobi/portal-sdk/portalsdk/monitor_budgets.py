from django.contrib.auth.models import User
from notification import send_notification
from portalsdk import APIContext, APIMethodType, APIRequest
import time
from mpesa_transaction import fetch_mpesa_transactions

# Function to continuously fetch transactions and monitor budgets
def monitor_budgets():
    while True:
        for user in User.objects.all():
            fetch_mpesa_transactions(user)
        time.sleep(86400)  # Fetch transactions once a day

if __name__ == '__main__':
    monitor_budgets()  # Start monitoring budgets