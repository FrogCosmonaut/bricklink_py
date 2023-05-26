import json

from urllib.parse import urljoin, urlencode

from . import config

def request(method: str, oauth_session: object, uri: str,
            params: dict = {}, body: dict = {}):
    """Send a request to the specified URI using the provided
    method and OAuth session.

    Arguments:
        method -- The HTTP method to use for the request.
        oauth_session -- The OAuth object used for authentication.
        uri -- The URI to send the request to.

    Keyword Arguments:
        params -- The parameters to include in the request. (default: {{}})
        body -- The body to include in the request data. (default: {{}})

    Raises:
        Exception: If the response code is not 200 (Bad request).

    Returns:
        requests.Response: The response object returned from the request.
    """

    headers = {}
    json_body = {}
   
    filtered_params = {k: v for k, v in params.items() if v is not None}
    params = urlencode(filtered_params, doseq=True)

    if body:
        headers = {'Content-Type' : 'application/json'}
        json_body = json.dumps(body)

    url = f"{urljoin(config.API_BASE_URL, f'{uri}?{params}')}"

    response = oauth_session.request(method, url, data=json_body,
                                    headers=headers)
    response_json = response.json()
    response_code = response_json['meta']['code']
    response_msg = response_json['meta']['message']

    if response_code == 200:
        return response_json['data']
    
    raise Exception(f'{response_code} Bad request: {response_msg}')