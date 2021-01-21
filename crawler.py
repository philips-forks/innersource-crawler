#!/usr/bin/env python

import os
from os.path import dirname, join

import github3
from dotenv import load_dotenv
import json

if __name__ == "__main__":

    # Load env variables from file
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    # Auth to GitHub.com
    gh = github3.login(token=os.getenv("GH_TOKEN"))

    # Get all repos from organization
    all_repos = gh.repositories()

    repo_list = []
    # Set the topic
    topic = os.getenv("TOPIC")

    for repo in all_repos:
        if repo is not None:
            # Get the repo topics as type dict and print them nicely

            # TODO: #6 handle rate limiting
            try:
                repo_topic = repo.topics()
            except Exception:
                print("skipping 404")
            else:
                if topic in repo_topic.names:
                    # TODO: #7 For each resulting project add a key _InnerSourceMetadata to the result from the GitHub API call and fill it with additional metadata about the project:
                    # TODO: - Check if there is a file innersource.json in the repository and add all keys directly below _InnerSourceMetadata.
                    # TODO: - Query GitHub for the weekly commit count (subset "all") and add it with the key participation
                    # TODO: - Check if there is a file CONTRIBUTING.md in the repository and add it with the key guidelines, value CONTRIBUTING.md
                    # TODO: Example available at https://github.com/SAP/project-portal-for-innersource/blob/main/repos.json
                    print("{0}".format(repo))
                    full_repository = repo.refresh()
                    # Add stuff here about innersource.json data before appending to list
                    repo_list.append(full_repository.as_dict())

    # Write each repository to a repos.json file
    with open("repos.json", "w") as f:
        json.dump(repo_list, f, indent=4)
