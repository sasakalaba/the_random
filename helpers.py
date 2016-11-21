import json
from requests import PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.compat import OrderedDict
from requests.cookies import RequestsCookieJar


def generate_request(method, url, body):
    """
    Generate our own custom request, so we can calculate digest auth.
    """
    method = method.upper()
    url = url
    files = []
    body = body
    json_string = None
    headers = CaseInsensitiveDict({
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Content-Length': str(len(json.dumps(body))),
        'Content-Type': 'application/json',
        'User-Agent': 'custom_user_agent'
    })
    params = OrderedDict()
    auth = {
        'id': '34T89RR6UW2JWTTUCB0CF8D87',
        'secret': 'm2dPlw8ql20JdyPKA5uUB3Ppgs4nNSp45IJsqRRdp0g'}
    cookies = RequestsCookieJar()
    hooks = {'response': []}

    pr = PreparedRequest()
    pr.prepare(
        method=method.upper(),
        url=url,
        files=files,
        data=json.dumps(body),
        json=json_string,
        headers=headers,
        params=params,
        auth=auth,
        cookies=cookies,
        hooks=hooks,
    )

    return pr


def assert_request(req, resp, expected_req, expected_resp):
    """
    Make sure that the request and response match the one we are trying to get.
    """
    def assert_headers(headers, expected_headers):
        x_date = headers.pop('expected_value')
        x_date_expected = expected_headers.pop('expected_value')
        auth = headers.pop('Authorization')
        auth_expected = expected_headers.pop('Authorization')

        assert len(x_date) == len(x_date_expected)
        assert len(auth) == len(auth_expected)
        assert headers == expected_headers

    # Compare requests
    attrs = ['url', 'method', 'body']

    for attr in attrs:
        value = getattr(req, attr)
        expected_value = getattr(expected_req, attr)

        if attr == 'body':
            assert json.loads(value) == json.loads(expected_value)
        elif attr == 'headers':
            assert_headers(value, expected_value)
        else:
            assert value == expected_value

    # Compare responses
    attrs = ['url', 'status_code', 'content']

    for attr in attrs:
        value = getattr(resp, attr)
        expected_value = expected_resp.get(attr)

        if attr == 'content':
            assert json.loads(value) == expected_value
        else:
            assert value == expected_value
