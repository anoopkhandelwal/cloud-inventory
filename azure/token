import adal
import requests


class AzureToken:

    def __init__(self):
        self.authentication_endpoint = 'https://login.microsoftonline.com/'
        self.resource = 'https://management.core.windows.net/'
        # self.resource = "https://graph.windows.net/"
        self.client_id = ""  # k.get("appKey")
        self.client_key = ""  # k.get("secretKey")
        self.tenant_id = ""
        self.context = adal.AuthenticationContext(self.authentication_endpoint + self.tenant_id )
        self.token_response = self.context.acquire_token_with_client_credentials(self.resource, self.client_id, self.client_key)

        self.access_token = self.token_response.get('accessToken')
        print(self.access_token)
        self.endpoint_ratecard =""
        self.endpoint_usage = ""

        self.headers = {"Authorization": 'Bearer ' + self.access_token, "Content-type": "application/json"}


token = AzureToken()
