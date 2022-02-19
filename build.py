#!/usr/bin/env python
# Copyright © 2020-2022 Hugo Locurcio and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import dateutil.parser as dateutil_parser
import json
import os
from typing import Any, List

import requests


def get_label_code(label_name: str) -> int:
    """
    Returns a code for a GitHub issue label to be added to the output JSON.
    This makes the JSON smaller and therefore faster to download and parse.
    NOTE: This must be kept in sync with `getLabelName()` in `index.html`.
    """
    if label_name == "meta":
        return 0

    if label_name == "topic:animation":
        return 1
    if label_name == "topic:assetlib":
        return 2
    if label_name == "topic:audio":
        return 3
    if label_name == "topic:buildsystem":
        return 4
    if label_name == "topic:codestyle":
        return 5
    if label_name == "topic:core":
        return 6
    if label_name == "topic:docs":
        return 7
    if label_name == "topic:editor":
        return 8
    if label_name == "topic:export":
        return 9
    if label_name == "topic:gdnative":
        return 10
    if label_name == "topic:gdscript":
        return 11
    if label_name == "topic:gui":
        return 12
    if label_name == "topic:import":
        return 13
    if label_name == "topic:input":
        return 14
    if label_name == "topic:mono":
        return 15
    if label_name == "topic:navigation":
        return 16
    if label_name == "topic:network":
        return 17
    if label_name == "topic:physics":
        return 18
    if label_name == "topic:plugin":
        return 19
    if label_name == "topic:porting":
        return 20
    if label_name == "topic:rendering":
        return 21
    if label_name == "topic:shaders":
        return 22
    if label_name == "topic:tests":
        return 23
    if label_name == "topic:visualscript":
        return 24
    if label_name == "topic:xr":
        return 25
    if label_name == "topic:2d":
        return 26
    if label_name == "topic:3d":
        return 27

    if label_name == "platform:windows":
        return 80
    if label_name == "platform:macos":
        return 81
    if label_name == "platform:linuxbsd":
        return 82
    if label_name == "platform:android":
        return 83
    if label_name == "platform:ios":
        return 84
    if label_name == "platform:html5":
        return 85
    if label_name == "platform:uwp":
        return 86

    print(
        f"WARNING: Unknown label name (no code assigned in `get_label_code()`): {label_name}"
    )
    return -1


def main() -> None:
    # Change to the directory where the script is located,
    # so that the script can be run from any location.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    print("[*] Fetching proposal JSON pages...")

    all_proposals: List[List[Any]] = []

    page = 1
    # We'll set the number of pages to a "finite" number once we make a request.
    num_pages = 10000

    while page <= num_pages:
        if num_pages == 10000:
            print(f"    Requesting batch of proposals {page}...")
        else:
            print(f"    Requesting batch of proposals {page}/{num_pages}...")
        request = requests.get(
            f"https://api.github.com/repos/godotengine/godot-proposals/issues?state=open&per_page=100&page={page}",
            headers={"Accept": "application/vnd.github.squirrel-girl-preview"},
        )

        if num_pages == 10000:
            # We don't know the number of pages yet, so figure it out.
            links_in_header = request.headers["Link"].split(",")
            for link in links_in_header:
                if '"last"' in link:
                    # Get the page number after the `page` query parameter.
                    num_pages = int(link.split("&page")[1][1:3])

        request_dict = json.loads(request.text)

        for proposal in request_dict:
            # Only include fields we use on the frontend.
            # Use an optimized array form to avoid including dozens of thousands
            # of string keys in the JSON.
            # Store the creation date as an UNIX timestamp integer as it's smaller than an ISO 8601 string.
            all_proposals.append(
                [
                    proposal["number"],
                    proposal["title"],
                    int(dateutil_parser.parse(proposal["created_at"]).strftime("%s")),
                    proposal["user"]["login"],
                    proposal["comments"],
                    [get_label_code(label["name"]) for label in proposal["labels"]],
                    [proposal["reactions"]["+1"], proposal["reactions"]["-1"]],
                ]
            )

        page += 1

    print("[*] Saving proposals.json...")

    with open("proposals.json", "w") as file:
        json.dump(all_proposals, file)

    print("[*] Success!")


if __name__ == "__main__":
    main()
