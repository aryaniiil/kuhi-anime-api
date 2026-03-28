import httpx
from fastapi import HTTPException
from src.config import ANILIST_URL, iter_miruro_pipe_targets
from src.parser import encode_pipe_request, decode_pipe_response, deep_translate

# function to run queries on anilist servers and return json data
async def anilist_query(query: str, variables: dict = None):
    # bundle everything together nicely
    body = {"query": query}
    if variables:
        body["variables"] = variables
        
    async with httpx.AsyncClient(timeout=15.0) as client:
        res = await client.post(ANILIST_URL, json=body)
        if res.status_code != 200:
            raise HTTPException(status_code=500, detail="anilist query failed")
        return res.json().get("data", {})

# fetch raw decrypted eps from miruro using their secret pipe
async def fetch_raw_episodes(anilist_id: int) -> dict:
    payload = {
        "path": "episodes",
        "method": "GET",
        "query": {"anilistId": anilist_id},
        "body": None,
        "version": "0.1.0",
    }
    encoded_req = encode_pipe_request(payload)
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        last_status = None
        for pipe_target, headers in iter_miruro_pipe_targets(encoded_req):
            print(f"\n[KUHI API] executing pipe for raw episodes:", pipe_target)
            res = await client.get(pipe_target, headers=headers)
            last_status = res.status_code
            if res.status_code == 200:
                data = decode_pipe_response(res.text.strip())
                deep_translate(data)
                return data

        raise HTTPException(status_code=last_status or 502, detail="pipe request failed")
