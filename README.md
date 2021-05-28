# `tube-cli`

A small Python script for downloading videos from [tube.tugraz.at](https://tube.tugraz.at).

## THIS REPOSITORY IS OBSOLETE

This repository is obsoleted by the `youtube-dl` support for
[tube.tugraz.at](https://tube.tugraz.at) in
[Ferdi265/youtube-dl](https://github.com/Ferdi265/youtube-dl/tree/tubetugraz).

## Installation

This script requires the `requests` package. Install the required dependencies
with `pip install -r requirements.txt`. The `series-download` and
`episode-download` commands require `curl` to be installed.

## Usage

You can run the script with `./tube-cli.py [args]` or `python3 tube-cli.py
[args]`.

```
usage: tube-cli.py [command] [args]
COMMANDS:
- series-download-urls <sid> [count] [offset]
- series-download <sid> [count] [offset]
- episode-download-url <id>
- episode-download <id>
```

The script will ask for the TUGrazOnline username and password to log in to
TUbe. This is required to list episodes and find download URLs. The URLs
themselves are usable without logging in.

## Episode and Series IDs

You can get the ids form the URL in TUbe, for example:

```
https://tube.tugraz.at/paella/ui/browse.html?series=b3ee3d02-8f13-453c-8dbd-789dda529f4a
https://tube.tugraz.at/paella/ui/watch.html?id=a8e73aee-ed27-4ef8-864d-a9bcbfe14881
```

- in the first URL, `b3ee3d02-8f13-453c-8dbd-789dda529f4a` (the part after
`series=`) is a series ID (sid).
- in the second URL, `a8e73aee-ed27-4ef8-864d-a9bcbfe14881` (the part after
`id=`) is an episode ID (id).
