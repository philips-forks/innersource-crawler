#!/usr/bin/env python

import json
import logging
import math
import os
import time
from base64 import b64decode
from functools import reduce
from os.path import dirname, join

import dateutil.parser as dp
import github3
from dotenv import load_dotenv

from lib import calculate_score

if __name__ == "__main__":

    # Load env variables from file
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    # Auth to GitHub.com
    gh = github3.login(token=os.getenv("GH_TOKEN"))

    query = os.getenv("QUERY")
    organization = os.getenv("ORGANIZATION")

    # Get all repos from organization
    search_string = "org:{} {}".format(organization, query)
    print("Search query: {0}".format(search_string))

    all_repos = gh.search_repositories(search_string)
    repo_list = []

    for repo in all_repos:
        if repo is not None:
            print("{0}".format(repo.repository))
            # print("{0}".format(calculateScore(repo)))
            full_repository = repo.repository.refresh()

            innersource_repo = repo.as_dict()
            innersource_repo["_InnerSourceMetadata"] = {}

            # fetch innersource.json
            try:
                content = repo.repository.file_contents("/innersource.json").content
                metadata = json.loads(b64decode(content))

                innersource_repo["_InnerSourceMetadata"] = metadata
            except github3.exceptions.NotFoundError:
                # innersource.json not found in repository, but it's not required
                pass

            # fetch repository participation
            participation = repo.repository.weekly_commit_count()
            innersource_repo["_InnerSourceMetadata"]["participation"] = participation[
                "all"
            ]

            # fetch contributing guidelines
            try:
                # if CONTRIBUTING.md exists in the repository, link to that instead of repo root
                content = repo.repository.file_contents("/CONTRIBUTING.md").content
                innersource_repo["_InnerSourceMetadata"][
                    "guidelines"
                ] = "CONTRIBUTING.md"
            except github3.exceptions.NotFoundError:
                # CONTRIBUTING.md not found in repository, but it's not required
                pass

            # fetch repository topics
            topics = repo.repository.topics()
            innersource_repo["_InnerSourceMetadata"]["topics"] = topics.names

            repo_list.append(innersource_repo)
            calculate_score(repo)

    # Write each repository to a repos.json file
    with open("repos.json", "w") as f:
        json.dump(repo_list, f, indent=4)
