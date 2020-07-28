import json
from oauthlib.oauth2 import WebApplicationClient
import requests
from urllib.parse import urljoin, urlparse


class OAuth2:

    def __init__(
            self, *,
            client_id: str, client_secret: str,
            authorization_url: str, token_url: str,
            userinfo_url: str, scope: list
            ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
        self.scope = scope
        # see https://oauthlib.readthedocs.io/en/latest/oauth2/clients/webapplicationclient.html # noqa
        self.oauth2_client = WebApplicationClient(client_id)

    def get_redirect_url(self, callback_url: str):

        # Prepare the authorization code request URI
        request_uri = self.oauth2_client.prepare_request_uri(
            self.authorization_url,
            redirect_uri=callback_url,
            scope=self.scope
        )

        return request_uri

    def get_user_info(self, request_url: str, code: str) -> dict:
        # Get request url without query parameter
        base_url = urljoin(request_url, urlparse(request_url).path)

        # Prepare a token creation request.
        token_url, headers, body = self.oauth2_client.prepare_token_request(
            self.token_url,
            authorization_response=request_url,
            redirect_url=base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.client_id, self.client_secret)
        )

        # Parse the JSON response body.
        self.oauth2_client.parse_request_body_response(
            json.dumps(token_response.json())
        )

        # Add token to the request uri, body or authorization header.
        uri, headers, body = self.oauth2_client.add_token(
            self.userinfo_url
        )
        userinfo_response = requests.get(uri, headers=headers, data=body)

        return userinfo_response.json()
