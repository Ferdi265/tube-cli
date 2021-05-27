#!/usr/bin/env python3
from typing import List, Tuple
from requests import Session
from getpass import getpass
import subprocess
import tube
import sys

def login() -> Session:
    username = input("username: ")
    password = getpass("password: ")
    return tube.login(username, password)

def parse_id_count_offset(args: List[str]) -> Tuple[str, int, int]:
    if len(args) < 1 or len(args) > 3:
        usage()

    id = args[0]

    if len(args) > 1:
        count = int(args[1])
    else:
        count = 100

    if len(args) > 2:
        offset = int(args[2])
    else:
        offset = 0

    return id, count, offset

def parse_id(args: List[str]) -> str:
    if len(args) != 1:
        usage()

    id = args[0]

    return id

def series_download_urls(args: List[str]):
    id, count, offset = parse_id_count_offset(args)

    s = login()
    eps = tube.get_series_episodes(s, id, count, offset)

    for ep in eps:
        print(tube.get_episode_download_url(ep))

def series_download(args: List[str]):
    id, count, offset = parse_id_count_offset(args)

    s = login()
    ser = tube.get_series(s, id)
    title = tube.get_series_title(ser)
    print(f">> series: {title}")

    eps = tube.get_series_episodes(s, id, count, offset)

    for i, ep in enumerate(eps):
        title = tube.get_episode_title(ep)
        url = tube.get_episode_download_url(ep)
        filename = tube.get_episode_download_filename(ep)
        print(f">> downloading [{i+1: 2d} / {len(eps): 2d}] {title}")
        subprocess.run(["curl", "--progress-bar", url, "-o", filename])

def episode_download_url(args: List[str]):
    id = parse_id(args)

    s = login()
    ep = tube.get_episode(s, id)
    print(tube.get_episode_download_url(ep))

def episode_download(args: List[str]):
    id = parse_id(args)

    s = login()
    ep = tube.get_episode(s, id)
    url = tube.get_episode_download_url(ep)
    *_, name = url.rsplit("/", 1)
    print(f">> downloading {name}")
    subprocess.run(["curl", "--progress-bar", url, "-o", name])

def usage():
    print("usage: tube-cli.py [command] [args]")
    print("COMMANDS:")
    print("- series-download-urls <sid> [count] [offset]")
    print("- series-download <sid> [count] [offset]")
    print("- episode-download-url <id>")
    print("- episode-download <id>")
    sys.exit(1)

def main(args: List[str]):
    if len(args) < 1:
        usage()

    subcmd, args = args[0], args[1:]
    if subcmd == "series-download-urls":
        series_download_urls(args)
    elif subcmd == "series-download":
        series_download(args)
    elif subcmd == "episode-download-url":
        episode_download_url(args)
    elif subcmd == "episode-download":
        episode_download(args)
    else:
        usage()

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
