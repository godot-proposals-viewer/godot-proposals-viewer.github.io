# Godot proposals viewer

View the current Godot proposals in a convenient way.

## How it works

- First, `build.py` downloads all open proposals from the GitHub API, in batches
  of 100 (the highest per-page limit allowed). The result is concatenated into a
  single JSON file with unused fields pruned.
- The JSON file and static HTML are deployed to GitHub Pages.
- The website uses [Alpine.js](https://github.com/alpinejs/alpine) and
  [Ky](https://github.com/sindresorhus/ky) to fetch the JSON from GitHub Pages
  and display it dynamically. This requires JavaScript to be enabled on the
  client.

Every day, there's a continuous integration step that runs the tasks above to
keep the page up-to-date.

## Development

Follow these instructions to set up this site locally for development purposes:

- Make sure you have Python 3.6 or later and pip.
- Install dependencies by running `pip install -r requirements.txt`.
- Run `build.py` to fetch proposals from the GitHub API. It makes a few dozen
  requests, which means you don't need to set up API authentication to bypass
  GitHub's 60 requests/hour limit.
- Start a local web server in the root directory then browse `index.html`.

## License

Copyright © 2020-2021 Hugo Locurcio and contributors

Unless otherwise specified, files in this repository are licensed under the
MIT license. See [LICENSE.md](LICENSE.md) for more information.
