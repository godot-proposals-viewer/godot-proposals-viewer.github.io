#!/usr/bin/env python3
# Copyright © 2020-present Hugo Locurcio and contributors
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

import json
import os
from typing import Any, List

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from typing_extensions import Final

import dateutil.parser as dateutil_parser


def get_label_code(label_name: str) -> int:
    """
    Returns a code for a GitHub issue label to be added to the output JSON.
    This makes the JSON smaller and therefore faster to download and parse.
    NOTE: This must be kept in sync with `getLabelName()` in `index.html`.
    """
    if label_name == "meta":
        return 0

    # Topic
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
    if label_name == "topic:gdextension":
        return 10
    if label_name == "topic:gdscript":
        return 11
    if label_name == "topic:gui":
        return 12
    if label_name == "topic:i18n":
        return 13
    if label_name == "topic:import":
        return 14
    if label_name == "topic:input":
        return 15
    if label_name == "topic:dotnet":
        return 16
    if label_name == "topic:navigation":
        return 17
    if label_name == "topic:network":
        return 18
    if label_name == "topic:physics":
        return 19
    if label_name == "topic:plugin":
        return 20
    if label_name == "topic:platforms":
        return 21
    if label_name == "topic:rendering":
        return 22
    if label_name == "topic:shaders":
        return 23
    if label_name == "topic:tests":
        return 24
    if label_name == "topic:visualscript":
        return 25
    if label_name == "topic:xr":
        return 26
    if label_name == "topic:2d":
        return 27
    if label_name == "topic:3d":
        return 28
    if label_name == "topic:particles":
        return 29
    if label_name == "topic:multiplayer":
        return 30

    # Status
    if label_name == "implementer wanted":
        return 60
    if label_name == "requires core feedback":
        return 61

    # Type
    if label_name == "usability":
        return 70
    if label_name == "performance":
        return 71
    if label_name == "breaks compat":
        return 72

    # Platform
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
    if label_name == "platform:visionos":
        return 85
    if label_name == "platform:web":
        return 86
    if label_name == "platform:uwp":
        return 87

    print(f"WARNING: Unknown label name (no code assigned in `get_label_code()`): {label_name}")
    return -1


def main() -> None:
    # Change to the directory where the script is located,
    # so that the script can be run from any location.
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    load_dotenv()

    transport: Final = AIOHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {os.getenv('GODOT_PROPOSALS_VIEWER_GITHUB_TOKEN')}"},
        ssl=True,
    )
    client: Final = Client(transport=transport, fetch_schema_from_transport=True)

    cursor = None

    proposals: List[List[Any]] = []

    # We'll set the number of pages to a "finite" number once we make a request.
    num_queries = 10000

    # Get all proposals.
    # TODO: Retry requests a few times if they fail.
    for i in range(num_queries):
        print(f"Requesting batch of proposals {i + 1}...")
        query = gql(
            """
query ($cursor: String) {
    repository(owner: "godotengine", name: "godot-proposals") {
        issues(last: 100, states: OPEN, orderBy: { direction: ASC, field: CREATED_AT }, before: $cursor) {
            edges {
                cursor
                node {
                    number
                    title
                    createdAt
                    author {
                        login
                    }
                    labels(first: 100) {
                        nodes {
                            name
                        }
                    }
                    reactionGroups {
                        content
                        users {
                            totalCount
                        }
                    }
                    comments {
                        totalCount
                    }
                }
            }
        }
    }
}
            """
        )

        # We're querying the first page, so we don't need to supply a valid cursor.
        # GQL will take care of not submitting the variable if it's set to `None`.
        result = client.execute(query, variable_values={"cursor": cursor})
        if result["repository"]["issues"]["edges"] != []:
            for edge in result["repository"]["issues"]["edges"]:
                proposal = edge["node"]
                thumbs_up_reactions = 0
                thumbs_down_reactions = 0
                for reaction_group in proposal["reactionGroups"]:
                    if reaction_group["content"] == "THUMBS_UP":
                        thumbs_up_reactions = reaction_group["users"]["totalCount"]
                    if reaction_group["content"] == "THUMBS_DOWN":
                        thumbs_down_reactions = reaction_group["users"]["totalCount"]

                # Only include fields we use on the frontend.
                # Use an optimized array form to avoid including dozens of thousands
                # of string keys in the JSON.
                # Store the creation date as an UNIX timestamp integer as it's smaller than an ISO 8601 string.
                proposals.append(
                    [
                        proposal["number"],
                        proposal["title"],
                        int(dateutil_parser.parse(proposal["createdAt"]).strftime("%s")),
                        proposal["author"]["login"] if proposal["author"] is not None else "ghost",
                        proposal["comments"]["totalCount"],
                        [get_label_code(label["name"]) for label in proposal["labels"]["nodes"]],
                        [thumbs_up_reactions, thumbs_down_reactions],
                    ]
                )

            # Get the cursor value of the last returned item, as we need it for subsequent requests (pagination).
            cursor = result["repository"]["issues"]["edges"][0]["cursor"]
        else:
            print("No more proposals to fetch.")
            break

    print("Saving proposals.json...")

    output_path: Final = "proposals.json"
    with open("proposals.json", "w") as file:
        json.dump(proposals, file)

    print(f"Wrote proposals to: {output_path}")


if __name__ == "__main__":
    main()
