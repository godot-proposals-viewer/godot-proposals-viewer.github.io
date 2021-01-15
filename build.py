#!/usr/bin/env python

import json
import os

import requests
from typing import List, Dict
from typing_extensions import Final

# 1 page fetches 100 proposals. Remember to increment the number below periodically
# to match the number of currently open proposals on
# https://github.com/godotengine/godot-proposals/issues.
NUM_PAGES: Final = 15


def main() -> None:
    # Change to the directory where the script is located,
    # so that the script can be run from any location.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    print("[*] Fetching proposal JSON pages...")

    all_proposals: List[Dict] = []

    for page in range(1, NUM_PAGES + 1):
        print(f"    Requesting batch of proposals {page}/{NUM_PAGES}...")
        request = requests.get(
            f"https://api.github.com/repos/godotengine/godot-proposals/issues?state=open&per_page=100&page={page}",
            headers={"Accept": "application/vnd.github.squirrel-girl-preview"},
        )
        request_dict = json.loads(request.text)

        for proposal in request_dict:
            # Only include fields we use on the frontend.
            all_proposals.append(
                {
                    "id": proposal["id"],
                    "number": proposal["number"],
                    "title": proposal["title"],
                    "created_at": proposal["created_at"],
                    "html_url": proposal["html_url"],
                    "user": {"login": proposal["user"]["login"]},
                    "comments": proposal["comments"],
                    "reactions": {
                        "+1": proposal["reactions"]["+1"],
                        "-1": proposal["reactions"]["-1"],
                    },
                }
            )

    print("[*] Saving proposals.json...")

    with open("proposals.json", "w") as file:
        json.dump(all_proposals, file)

    print("[*] Success!")


if __name__ == "__main__":
    main()
