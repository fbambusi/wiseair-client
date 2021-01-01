import requests
import json
import urllib


class IdoClient(object):
    app_client_id = None
    app_client_secret = None
    api_key = None
    base_url = None
    desired_resources = None

    stage = None

    def __init__(self, app_client_id, app_client_secret, api_key, stage="prod", needs_auth=True, desired_resources=[]):
        self.app_client_secret = app_client_secret
        self.api_key = api_key
        self.app_client_id = app_client_id
        self.stage = stage
        self.desired_resources = desired_resources
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
            TOKEN_ENDPOINT = "https://ido.auth.eu-central-1.amazoncognito.com/token"
        else:
            TOKEN_ENDPOINT = "https://ido-stage.auth.eu-central-1.amazoncognito.com/token"

        scope = " ".join([f"{self.base_url}/{r}.read" for r in self.desired_resources])
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.app_client_id,
            'client_secret': self.app_client_secret,
            'scope': scope
        }
        response = requests.post(TOKEN_ENDPOINT, data=body)
        tok = json.loads(response.text)

        self.id_token = tok["access_token"]

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
        return json.loads(self.authenticated_get(f"{self.base_url}/{resource_name}?{qps}").decode("utf-8"))
