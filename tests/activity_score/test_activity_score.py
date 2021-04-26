import pytest

from lib import calculate_score


class Repo:
    def __init__(self, forks_count, watchers_count, stargazers_count, open_issues_count, updated_at, created_at, description):
        self.forks_count = forks_count
        self.watchers_count = watchers_count
        self.stargazers_count = stargazers_count
        self.open_issues_count = open_issues_count
        self.updated_at = updated_at
        self.created_at = created_at
        self.description = description
        self._InnerSourceMetadata = {
            'participation': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'motivation': "",
            'guidelines': ""}


@pytest.fixture
def empty_repo():
    return Repo(0, 0, 0, 0, "2020-04-17T16:09:26Z", "2020-01-27T09:32:01Z", "Description")


@pytest.fixture
def small_activity_repo():
    return Repo(1, 1, 1, 1, "2020-04-18T16:09:26Z", "2020-01-25T09:32:01Z", "Description")


def test_calculate_score_empty(empty_repo):
    """
    Test calculate_actvitiy if no data is available
    """
    assert calculate_score(empty_repo) == 0


def test_calculate_score_small(small_activity_repo):
    """
    Test calculate_actvitiy if no data is available
    """
    assert calculate_score(small_activity_repo) == 7
