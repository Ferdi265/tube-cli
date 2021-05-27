from typing import Optional, List, Dict, Any
from requests import Session
import requests as rq
import json

def login(username: str, password: str) -> Session:
    s = Session()

    r1 = s.get("https://tube.tugraz.at/Shibboleth.sso/Login?target=/paella/ui/index.html")
    if r1.status_code != 200:
        raise ValueError(f"failed to load login page, error code: {r1.status_code}")

    r2 = s.post(r1.url, data = {
        "lang": "de",
        "_eventId_proceed": "",
        "j_username": username,
        "j_password": password
    }, headers = { "referer": r1.url })
    if r2.status_code != 200:
        raise ValueError(f"failed to login, error code: {r2.status_code}")

    if r2.url != "https://tube.tugraz.at/paella/ui/index.html":
        raise ValueError(f"failed to login, URL does not match: {r2.url}")

    return s

def get_series(s: Session, id: str, count: int = 100, sort: str = "TITLE") -> Dict[str, Any]:
    r = s.get("https://tube.tugraz.at/series/series.json", params = {
        "sort": sort,
        "count": count,
        "seriesId": id
    })

    if r.status_code != 200:
        raise ValueError(f"failed to load series, error code: {r.status_code}")

    return json.loads(r.text)

def get_series_episodes(s: Session, id: str, count: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    r = s.get("https://tube.tugraz.at/search/episode.json", params = {
        "sid": id,
        "limit": count,
        "offset": offset
    })

    if r.status_code != 200:
        raise ValueError(f"failed to load episodes, error code: {r.status_code}")

    return json.loads(r.text)["search-results"]["result"]

def get_episode(s: Session, id: str, count: int = 100, offset: int = 0) -> Dict[str, Any]:
    r = s.get("https://tube.tugraz.at/search/episode.json", params = {
        "id": id,
        "limit": count,
        "offset": offset
    })

    if r.status_code != 200:
        raise ValueError(f"failed to load episodes, error code: {r.status_code}")

    return json.loads(r.text)["search-results"]["result"][0]

def get_episode_download_url(episode: Dict[str, Any]) -> str:
    return episode['mediapackage']['media']['track'][0]['url']
