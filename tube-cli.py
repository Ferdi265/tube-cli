#!/usr/bin/env python3
from typing import List, Tuple
from requests import Session
from getpass import getpass
import subprocess
import tube
import sys

def usage():
    print("usage: tube-cli.py [command] [args]")
    print("COMMANDS:")
    print("- download-episode-urls <id> [count] [offset]")
    print("- download-episodes <id> [count] [offset]")
    sys.exit(1)

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

def download_episode_urls(args: List[str]):
    id, count, offset = parse_id_count_offset(args)

    s = login()
    eps = tube.get_episodes(s, id, count, offset)

    for ep in eps:
        print(tube.get_episode_download_url(ep))

def download_episodes(args: List[str]):
    id, count, offset = parse_id_count_offset(args)

    s = login()
    eps = tube.get_episodes(s, id, count, offset)

    for i, ep in enumerate(eps):
        url = tube.get_episode_download_url(ep)
        *_, name = url.rsplit("/", 1)
        print(f">> downloading [{i+1: 2d} / {len(eps): 2d}] {name}")
        subprocess.run(["curl", "--progress-bar", url, "-o", name])

def main(args: List[str]):
    if len(args) < 1:
        usage()

    subcmd, args = args[0], args[1:]
    if subcmd == "download-episode-urls":
        download_episode_urls(args)
    elif subcmd == "download-episodes":
        download_episodes(args)
    else:
        usage()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
