# Godot proposals viewer

View the current Godot proposals in a convenient way.

## Development

Follow these instructions to set up this site locally for development purposes:

- Run `build.sh` to fetch proposals from the GitHub API. It makes a few dozen
  requests, requests, which means you don't need to set up API authentication to
  bypass GitHub's 60 requests/hour limit.
- Start a local web server in the root directory then browse `index.html`.

## License

Copyright © 2020 Hugo Locurcio and contributors

Unless otherwise specified, files in this repository are licensed under the
MIT license. See [LICENSE.md](LICENSE.md) for more information.
