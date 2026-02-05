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

## Local development

First, make sure you have [Python](https://www.python.org) installed (3.6 or later).

You could install the requirements directly from `requirements.txt`, but we recommend
you use a virtual environment to do it:

```shell
virtualenv .venv --python python3
source .venv/bin/activate
pip install -r requirements.txt
```

Before you can test locally, you need a `proposals.json` file. The easiest way
to get it is to download it from the latest automated fetch. To do this, visit
this repository's [Actions](https://github.com/godot-proposals-viewer/godot-proposals-viewer.github.io/actions),
click the latest, and download the linked artifact. Alternatively, you can use
`python build.py` to fetch and create your own (although this requires a
GitHub GraphQL token; see [`.env.example`](.env.example)).

You can try the website locally by launching a local web server, for example:

```shell
python -m http.server 8000
```

## License

Copyright © 2020-present Hugo Locurcio and contributors

Unless otherwise specified, files in this repository are licensed under the
MIT license. See [LICENSE.md](LICENSE.md) for more information.
