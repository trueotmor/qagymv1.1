import requests
from typing import Optional, Dict, Any, Union

class APIClient:
    def __init__(self, base_url: str) -> None:
        self.session = requests.Session()
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = headers or self.headers
        print('client', url)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=headers,
            timeout=10
        )
        print('client', response)
        return response

    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        return self._request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        return self._request("POST", endpoint, json=json, data=data, headers=headers)

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        return self._request("PUT", endpoint, json=json, data=data, headers=headers)

    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        return self._request("PATCH", endpoint, json=json, data=data, headers=headers)

    def delete(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict] = None
    ) -> requests.Response:
        return self._request("DELETE", endpoint, json=json, data=data, headers=headers)