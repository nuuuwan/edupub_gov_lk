import requests
from bs4 import BeautifulSoup
from utils import Log

TIMEOUT = 30
TIMEOUT_DOWNLOAD_BINARY = 2 * 60
log = Log('WWW')


class WWW:
    def __init__(self, url):
        self.url = url

    def get(self, params=None):
        response = requests.get(self.url, params=params, timeout=TIMEOUT)
        html = response.text
        n_html = len(html) / 1_000_000
        soup = BeautifulSoup(html, "html.parser")
        log.debug(f"GET {self.url} {params} ({n_html:.3f}MB) complete.")

        return soup

    def post(self, data=None):
        response = requests.post(self.url, data=data, timeout=TIMEOUT)
        html = response.text
        n_html = len(html) / 1_000_000
        soup = BeautifulSoup(html, "html.parser")
        log.debug(f"POST {self.url} {data} ({n_html:.3f}MB) complete.")
        return soup

    def download_binary(self, local_path):
        log.debug(f"Downloading {self.url} to {local_path}...")
        response = requests.get(self.url, timeout=TIMEOUT_DOWNLOAD_BINARY)
        content = response.content
        n_content = len(content) / 1_000_000
        with open(local_path, 'wb') as fout:
            fout.write(content)
        log.debug(
            f"Downloaded {self.url} to {local_path} ({n_content:.3f}MB)."
        )

    def exists(self):
        response = requests.head(self.url)
        return response.status_code == 200
