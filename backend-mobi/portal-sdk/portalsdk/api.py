import json
from enum import Enum
from pprint import pprint

import requests
from base64 import b64decode, b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from portalsdk import APIContext, APIMethodType, APIRequest


#  This code includes classes and functions for creating API requests,
#  handling API responses, and managing API context. 
#  It uses encryption to create a bearer token, 
#  allows you to specify the HTTP method 
#  by (GET, POST, PUT), URL, headers, and parameters for API requests.

class APIRequest:

    def __init__(self, context=None):
        self.context = context

    def execute(self):
        if self.context is not None:
            self.create_default_headers()
            # pprint(self.context)
            try:
                return {
                    APIMethodType.GET: self.__get,
                    APIMethodType.POST: self.__post,
                    APIMethodType.PUT: self.__put
                }.get(self.context.method_type, self.__unknown)()
            except requests.exceptions.ConnectionError as ce:
                print(ce)
                return None
        else:
            raise TypeError('Context cannot be None.')

    def create_bearer_token(self):
        key_der = b64decode(self.context.public_key)
        key_pub = RSA.importKey(key_der)
        cipher = Cipher_PKCS1_v1_5.new(key_pub)
        cipher_text = cipher.encrypt(self.context.api_key.encode('ascii'))
        encrypted_msg = b64encode(cipher_text)

        return encrypted_msg

    def create_default_headers(self):
        self.context.add_header('Authorization', 'Bearer {}'.format(self.create_bearer_token().decode('utf-8')))
        self.context.add_header('Content-Type', 'application/json')
        self.context.add_header('Host', self.context.address)

    def __get(self):
        r = requests.get(self.context.get_url(), params=self.context.get_parameters(), headers=self.context.get_headers())
        print(r)
        return APIResponse(r.status_code, json.loads(r.headers.__str__().replace("'", '"')), json.loads(r.text))

    def __post(self):
        r = requests.post(self.context.get_url(), headers=self.context.get_headers(), json=self.context.get_parameters())
        print(r)
        return APIResponse(r.status_code, json.loads(r.headers.__str__().replace("'", '"')), json.loads(r.text))

    def __put(self):
        print('PUT')
        r = requests.put(self.context.get_url(), headers=self.context.get_headers(), json=self.context.get_parameters())
        print('PUT', r)
        return APIResponse(r.status_code, json.loads(r.headers.__str__().replace("'", '"')), json.loads(r.text))

    def __unknown(self):
        raise Exception('Unknown Method')
    
    # 
def get_transaction_statements(self):
    # Make a GET request to the M-Pesa API endpoint for transaction statements
    r = requests.get(self.context.get_url(), params=self.context.get_parameters(), headers=self.context.get_headers())

    if r.status_code == 200:
        # Successfully retrieved transaction statements
        transaction_statements = json.loads(r.text)
        return transaction_statements
    else:
        # Handle error cases, e.g., return an error message
        return {"error": "Failed to retrieve transaction statements"}

# Example usage
if __name__ == '__main__':
    # Create an APIContext with the necessary details
    api_context = APIContext(
        api_key='your_api_key', # edit right values
        public_key='your_public_key',
        ssl=True,
        method_type=APIMethodType.GET,
        address='m-pesa-api-url',
        port=443,
        path='/m-pesa/transaction-statements',
        headers={},
        parameters={'account_id': 'your_account_id', 'start_date': 'start_date', 'end_date': 'end_date'}
    )

    # Create an APIRequest instance with the context
    api_request = APIRequest(api_context)

    # Make the API request to retrieve transaction statements
    transaction_statements = api_request.get_transaction_statements()

    # Process and use the transaction statements as needed
    if "error" in transaction_statements:
        print("Error:", transaction_statements["error"])
    else:
        # Process the retrieved transaction statements
        pprint(transaction_statements)



class APIResponse(dict):

    def __init__(self, status_code, headers, body):
        super(APIResponse, self).__init__()
        self['status_code']: str = status_code
        self['headers']: dict = headers
        self['body']: dict = body

    @property
    def status_code(self) -> int:
        return self['status_code']

    @status_code.setter
    def status_code(self, status_code: int):
        if type(status_code) is not int:
            raise TypeError('status_code must be a int')
        else:
            self['status_code'] = status_code

    @property
    def headers(self) -> dict:
        return self['headers']

    @headers.setter
    def headers(self, headers: dict):
        if type(headers) is not dict:
            raise TypeError('headers must be a dict')
        else:
            self['headers'] = headers

    @property
    def body(self) -> dict:
        return self['body']

    @body.setter
    def body(self, body: dict):
        if type(body) is not dict:
            raise TypeError('body must be a dict')
        else:
            self['body'] = body


class APIMethodType(Enum):
    GET: int = 0
    POST: int = 1
    PUT: int = 3
    DELETE: int = 4


class APIContext(dict):

    def __init__(self, api_key='', public_key='', ssl=False, method_type=APIMethodType.GET, address='', port=80, path='', headers=None, parameters=None):
        super(APIContext, self).__init()

        self['api_key'] = api_key  # Removed the type annotation ': str'
        self['public_key'] = public_key  # Removed the type annotation ': str'
        self['ssl'] = ssl  # Removed the type annotation ': bool'
        self['method_type'] = method_type  # Removed the type annotation ': Enum'
        self['address'] = address  # Removed the type annotation ': str'
        self['port'] = port  # Removed the type annotation ': int'
        self['path'] = path  # Removed the type annotation ': str'
        self['headers'] = headers if headers is not None else {}  # Added a check for 'None'
        self['parameters'] = parameters if parameters is not None else {}  # Added a check for 'None'


        

    def get_url(self):
        if self.ssl is True:
            return 'https://{}:{}{}'.format(self.address, self.port, self.path)
        else:
            return 'http://{}:{}{}'.format(self.address, self.port, self.path)

    def add_header(self, header, value):
        self['headers'].update({header: value})

    def get_headers(self):
        return self['headers']

    def add_parameter(self, key, value):
        self['parameters'].update({key: value})

    def get_parameters(self):
        return self['parameters']

    @property
    def api_key(self) -> str:
        return self['api_key']

    @api_key.setter
    def api_key(self, api_key: str):
        if type(api_key) is not str:
            raise TypeError('api_key must be a str')
        else:
            self['api_key'] = api_key

    @property
    def public_key(self) -> str:
        return self['public_key']

    @public_key.setter
    def public_key(self, public_key: str):
        if type(public_key) is not str:
            raise TypeError('public_key must be a str')
        else:
            self['public_key'] = public_key

    @property
    def ssl(self) -> bool:
        return self['ssl']

    @ssl.setter
    def ssl(self, ssl: bool):
        if type(ssl) is not bool:
            raise TypeError('ssl must be a bool')
        else:
            self['ssl'] = ssl

    @property
    def method_type(self) -> APIMethodType:
        return self['method_type']

    @method_type.setter
    def method_type(self, method_type: APIMethodType):
        if type(method_type) is not APIMethodType:
            raise TypeError('method_type must be a APIMethodType')
        else:
            self['method_type'] = method_type

    @property
    def address(self) -> str:
        return self['address']

    @address.setter
    def address(self, address: str):
        if type(address) is not str:
            raise TypeError('address must be a str')
        else:
            self['address'] = address

    @property
    def port(self) -> int:
        return self['port']

    @port.setter
    def port(self, port: int):
        if type(port) is not int:
            raise TypeError('port must be a int')
        else:
            self['port'] = port

    @property
    def path(self) -> str:
        return self['path']

    @path.setter
    def path(self, path: str):
        if type(path) is not str:
            raise TypeError('path must be a str')
        else:
            self['path'] = path
