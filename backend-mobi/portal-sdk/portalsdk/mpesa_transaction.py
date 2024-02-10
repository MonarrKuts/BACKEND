
# mpesa_integration
from portalsdk import APIContext, APIMethodType, APIRequest
import time
from notification import send_notification

from django.contrib.auth.models import User  # Import the User model


def fetch_mpesa_transactions(user):
    # Set up the API context
    api_context = APIContext(api_key='6bc4157dbowkdd409118e0978dc6991a', public_key='MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ==', ssl=True, method_type=APIMethodType.GET, address='openapi.m-pesa.com', port=443, path='/sandbox/ipg/v2/vodafoneGHA/queryTransactionStatus/')
    
    # Add parameters, such as user identification, to the API request
    api_context.add_parameter('user_id', user.id)

    # Create an API request and execute it
    api_request = APIRequest(api_context)
    try:
        result = api_request.execute()
    except Exception as e:
        print('API call failed:', e)
        return

    # Process the API response (assuming it contains transaction data)
    transactions = result.body.get('transactions', [])
    
    # Process transactions and compare them with the user's budgets
    for transaction in transactions:
        # Compare the transaction amount with the user's budget and trigger notifications as needed
        Budget = Budget.objects.get(user=user, category=transaction['category'])
        if transaction['amount'] > Budget.amount:
            # Trigger a notification for exceeding the budget
            send_notification(User, f'You have exceeded your budget for {Budget.category}.')
        else:
            # Send a congratulatory message for staying within the budget
            (User, f'Great job! You are within your budget for {Budget.category}.')

while True:
    for user in User.objects.all():
        fetch_mpesa_transactions(user)
    time.sleep(86400)  # Fetch transactions once a day

