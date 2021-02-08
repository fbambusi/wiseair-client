import requests
import json
import urllib


class IdoUnauthorizedException(Exception):
    """
    The request is not authenticated.
    """
    pass


class IdoForbiddenException(Exception):
    """
    Forbidden means that even with a valid authentication the request may fail.
    """
    pass


class IdoClient(object):
    """
    A wrapper which allows users to query IDO backend using their credentials.
    """
    app_client_id = None
    app_client_secret = None
    api_key = None
    base_url = None
    desired_resources = None
    writable_resources = None
    stage = None

    def __init__(self, app_client_id, app_client_secret, api_key, stage="prod", needs_auth=True, desired_resources=[],
                 writable_resources=[]):
        self.app_client_secret = app_client_secret
        self.api_key = api_key
        self.app_client_id = app_client_id
        self.stage = stage
        self.desired_resources = desired_resources
        self.writable_resources = writable_resources
        if stage == "prod":
            self.base_url = "https://apiv1.ido.wiseair-api.com"
        else:
            self.base_url = "https://apiv1-stage.ido.wiseair-api.com"
        if needs_auth:
            self._get_token()

    def _get_token(self):
        """
        Get bearer token to sign subsequent requests
        :return:
        """
        if self.stage == "prod":
            TOKEN_ENDPOINT = "https://ido-api.auth.eu-central-1.amazoncognito.com/token"
        else:
            TOKEN_ENDPOINT = "https://ido-stage.auth.eu-central-1.amazoncognito.com/token"

        scope = " ".join(
            [f"{self.base_url}/{r}.read" for r in self.desired_resources] + [f"{self.base_url}/{r}.write" for r in
                                                                             self.writable_resources])

        body = {
            'grant_type': 'client_credentials',
            'client_id': self.app_client_id,
            'client_secret': self.app_client_secret,
            'scope': scope
        }
        response = requests.post(TOKEN_ENDPOINT, data=body)
        tok = json.loads(response.text)
        try:
            self.id_token = tok["access_token"]
        except KeyError:
            raise IdoForbiddenException(
                f"Could not get access token with the given credentials for the given scope {scope}")

    def _get_headers(self):
        headers = {
            "Authorization": "Bearer " + self.id_token}
        if self.api_key is not None:
            headers["x-api-key"] = self.api_key
        return headers

    def authenticated_get(self, url):
        """
        Perform a GET request, signing it with the internal bearer token
        :param url:
        :return:
        """

        resp = requests.get(url=url,
                            headers=self._get_headers())
        if resp.status_code == 401:
            raise IdoUnauthorizedException()
        if resp.status_code == 403:
            raise IdoForbiddenException(f"{url} could not be queried")
        return resp.content

    def authenticated_post(self, url, payload):
        """
        Perform a POST request, signing it with the internal bearer token
        :param url:
        :return:
        """
        resp = requests.post(url=url, json=payload,
                             headers=self._get_headers())
        return resp.content


    def authenticated_put(self, url, payload):
        """
        Perform a PUT request, signing it with the internal bearer token
        :param url:
        :return:
        """
        resp = requests.put(url=url, json=payload,
                             headers=self._get_headers())
        return resp.content

    def authenticated_patch(self, url, payload):
        """
        Perform a PATCH request, signing it with the internal bearer token
        :param url:
        :return:
        """
        resp = requests.patch(url=url, json=payload,
                             headers=self._get_headers())
        return resp.content


    def authenticated_delete(self, url):
        """
        Perform a DELETE request, signing it with the internal bearer token
        :param url:
        :return:
        """
        resp = requests.delete(url=url,headers=self._get_headers())
        return resp.content



    def simple_post(self, url, payload):
        """
        Perform a POST request with JSON content
        :param url:
        :return:
        """
        resp = requests.post(url=url, json=payload,
                             )
        return resp.content

    def simple_get(self, url):
        """
        Perform a POST request with JSON content
        :param url:
        :return:
        """
        resp = requests.get(url=url)
        return resp.content

    def simple_put(self, url, payload):
        """
        Perform a PUT request
        :param url:
        :return:
        """
        resp = requests.put(url=url, json=payload)
        return resp.content

    def simple_patch(self, url, payload):
        """
        Perform a PATCH request
        :param url:
        :return:
        """
        resp = requests.patch(url=url, json=payload)
        return resp.content


    def simple_delete(self, url,):
        """
        Perform a DELETE request
        :param url:
        :return:
        """
        resp = requests.delete(url=url)
        return resp.content

    def legacy_post(self, url, payload):
        """
        Perform a POST request with JSON content
        :param url:
        :return:
        """
        resp = requests.post(url=url, params=payload,
                             )
        return resp.content

    def query_resource(self, resource_name, query_parameters) -> dict:
        """
        Fetch all the resources that comply with a given set of criteria.
        :param resource_name:
        :param query_parameters:
        :return:
        """
        assert resource_name in self.desired_resources
        qps = urllib.parse.urlencode(query_parameters, doseq=False)
        url_1 = f"{self.base_url}/{resource_name}?{qps}"
        try:
            response = self.authenticated_get(url_1)
            return json.loads(response.decode("utf-8"))
        except IdoUnauthorizedException as e:
            url_2 = f"{self.base_url}/{resource_name}/scoped/query?{qps}"
            response = self.authenticated_get(url_2)
            return json.loads(response.decode("utf-8"))
