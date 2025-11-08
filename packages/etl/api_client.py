import time

import requests
import structlog
from requests import ConnectionError, RequestException, Response, Timeout

logger = structlog.get_logger(__name__)


class ThirdPartyAPI:
    def __init__(self, max_retries: int = 3, base_backoff: int = 2, timeout: int = 10) -> None:
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.timeout = timeout

    def api_call(
        self,
        url: str,
        method: str = "post",
        data: dict = None,
    ) -> Response:
        extra_args = {}
        if method == "post":
            extra_args = {"json": data}

        retries = 0
        while retries <= self.max_retries:
            try:
                response = getattr(requests, method)(
                    url,
                    **extra_args,
                )
                return response
            except RequestException as exc:
                wait_time = 2**retries
                logger.error(f"Error fetching {url}: {exc}. Retry {retries + 1}/{self.max_retries} in {wait_time}s")
                time.sleep(wait_time)
            except ValueError as exc:
                logger.error(f"Value error in {url}: {exc}")
                raise
            except (Timeout, ConnectionError) as exc:
                wait_time = self.base_backoff**retries
                logger.warning(
                    f"Transient error calling {url}: {exc}. Retry {retries + 1}/{self.max_retries} in {wait_time}s"
                )
                time.sleep(wait_time)

            retries += 1
            if retries >= self.max_retries:
                logger.error(f"Max retries reached for {url}. Failing permanently.")
                raise

        raise RuntimeError("api_call failed unexpectedly")


class DWDClient(ThirdPartyAPI):
    def get_text_data(
        self,
        url: str,
        method: str = "post",
        data: dict = None,
    ) -> str:
        response = self.api_call(url, method, data)

        return response.text

    def get_response_content(
        self,
        url: str,
        method: str = "post",
        data: dict = None,
    ) -> bytes:
        response = self.api_call(url, method, data)

        return response.content
