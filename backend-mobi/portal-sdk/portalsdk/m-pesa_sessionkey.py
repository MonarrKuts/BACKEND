from portalsdk import APIContext, APIMethodType, APIRequest
from time import sleep
from mpesa_transaction import fetch_mpesa_transactions

from portalsdk import APIContext, APIMethodType, APIRequest
import time



# this code interacts with M-pesa api to query transaction status and obtain a session key

def main():
    # Public key on the API listener used to encrypt keys
    public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ=='
    # Create Context with API to request a Session ID
    api_context = APIContext()
    # Session key
    api_context.api_key = '6bc4157dbowkdd409118e0978dc6991a'
    # Public key
    api_context.public_key = public_key
    # Use ssl/https
    api_context.ssl = True
    # Method type (can be GET/POST/PUT)
    api_context.method_type = APIMethodType.GET
    # API address
    api_context.address = 'openapi.m-pesa.com'
    # API Port
    api_context.port = 443
    # API Path
    api_context.path = '/sandbox/ipg/v2/vodafoneGHA/queryTransactionStatus/'

    # Add/update headers
    api_context.add_header('Origin', '*')

    # Parameters can be added to the call as well that on POST will be in JSON format and on GET will be URL parameters
    # api_context.add_parameter('key', 'value')
    api_context.add_parameter('input_QueryReference', '000000000000000000001')
    api_context.add_parameter('input_ServiceProviderCode', '000000')
    api_context.add_parameter('input_ThirdPartyConversationID', 'asv02e5958774f7ba228d83d0d689761')
    api_context.add_parameter('input_Country', 'GHA')

    # Do the API call and put the result in a response packet
    api_request = APIRequest(api_context)

    # Do the API call and put the result in a response packet
    result = None
    try:
        result = api_request.execute()
    except Exception as e:
        print('Call Failed: ' + e)

    if result is None:
        raise Exception('API call failed to get a result. Please check.')

    # Display results
    print(result.status_code)
    print(result.headers)
    print(result.body)

if __name__ == '__main__':
    main()
