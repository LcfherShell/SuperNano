try:
    import httpx as requests
except ImportError:
    import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
import importlib, inspect

DEFAULT_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "connection": "keep-alive",
}


class Fetch:
    def __init__(self, headers: dict = {}):
        self.headers = headers or DEFAULT_HEADERS
        try:
            self.sync_client = requests.Client(headers=self.headers)
            self.async_client = requests.AsyncClient(headers=self.headers)
        except AttributeError:
            self.sync_client = requests.Session()
            self.sync_client.headers.update(self.headers)
            self.async_client = self.sync_client

        def check_class_in_package(package_name, class_name):
            try:
                # Import the package
                package = importlib.import_module(package_name)
                # Cek apakah kelas ada di dalam modul
                if hasattr(package, class_name):
                    cls = getattr(package, class_name)
                    # Pastikan itu adalah kelas, bukan atribut atau fungsi
                    if inspect.isclass(cls):
                        return True, "ClassFound"
                return False, "ClassNotFound"
            except ModuleNotFoundError:
                return False, "ModuleNotFoundError"

        self.check_class_in_package = check_class_in_package

    def _request_sync(self, method, url, max_retries=5, timeout=5, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                response = self.sync_client.request(
                    method, url, timeout=timeout, **kwargs
                )
                response.raise_for_status()
                return response
            except (ConnectionError, Timeout) as e:
                retries += 1
                print(f"Connection failed ({e}). Retrying {retries}/{max_retries}...")
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                break
        raise Exception(f"Failed to connect to {url} after {max_retries} retries.")

    async def _request_async(self, method, url, max_retries=5, timeout=5, **kwargs):
        retries = 0
        itsAsync, _ = self.check_class_in_package(requests.__name__, "AsyncClient")
        while retries < max_retries:
            try:
                if itsAsync:
                    response = await self.async_client.request(
                        method, url, timeout=timeout, **kwargs
                    )
                else:
                    response = self.async_client.request(
                        method, url, timeout=timeout, **kwargs
                    )
                response.raise_for_status()
                return response
            except (ConnectionError, Timeout) as e:
                retries += 1
                print(f"Connection failed ({e}). Retrying {retries}/{max_retries}...")
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                break
        raise Exception(f"Failed to connect to {url} after {max_retries} retries.")

    def get(self, url, max_retries=5, timeout=5, async_mode=False, **kwargs):
        """Performs a GET request, either synchronously or asynchronously."""
        if async_mode:
            return self._request_async("GET", url, max_retries, timeout, **kwargs)
        else:
            return self._request_sync("GET", url, max_retries, timeout, **kwargs)

    def post(self, url, max_retries=5, timeout=5, async_mode=False, **kwargs):
        """Performs a POST request, either synchronously or asynchronously."""
        if async_mode:
            return self._request_async("POST", url, max_retries, timeout, **kwargs)
        else:
            return self._request_sync("POST", url, max_retries, timeout, **kwargs)

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.sync_client.close()

    async def __aenter__(self):
        """Enter the async runtime context related to this object."""
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Exit the async runtime context related to this object."""
        try:
            await self.async_client.aclose()
        except:
            self.async_client.close()
