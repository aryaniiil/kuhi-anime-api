# configuration of the app and constants for apis
# these are just standard headers we send
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

# legacy alias used by proxy endpoints
HEADERS = BASE_HEADERS

# the graph ql api url for fetching anime details
ANILIST_URL = "https://graphql.anilist.co"

# miruro base urls (ordered by preference)
MIRURO_BASE_URLS = [
    "https://www.miruro.online",
    "https://www.miruro.bz",
]

# backend pipe path of miruro
MIRURO_PIPE_PATH = "/api/secure/pipe"

def iter_miruro_pipe_targets(encoded_req: str):
    # yields (pipe_url, headers) in preferred order
    for base in MIRURO_BASE_URLS:
        pipe_url = f"{base}{MIRURO_PIPE_PATH}?e={encoded_req}"
        headers = {
            **BASE_HEADERS,
            "Referer": f"{base}/",
        }
        yield pipe_url, headers
