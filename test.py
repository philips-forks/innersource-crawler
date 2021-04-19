import unittest

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
                'participation': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                'motivation': "",
                'guidelines': ""}

class TestCalculateScore(unittest.TestCase):
    def test_calculate_score(self):
        """
        Test calculate_actvitiy if no data is available
        """
        repo = Repo(0,0,0,0,"2020-04-17T16:09:26Z", "2020-01-27T09:32:01Z")
        result = calculate_score(repo)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
