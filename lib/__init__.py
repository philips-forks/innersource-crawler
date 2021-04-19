import json
import os
import math
import time
import logging
import dateutil.parser as dp
from functools import reduce

def calculate_score(repo):
        iScore = 50
        iScore += (repo.forks_count * 5) + repo.watchers_count + (repo.stargazers_count / 3) + (repo.open_issues_count / 5)
        print("Repo Score after 1: {0}".format(iScore))
        iDaysSinceLastUpdate = (time.time() - dp.parse(repo.updated_at).timestamp()) / 86400
        print("Day since last update: {0}".format(iDaysSinceLastUpdate))
        iScore = iScore * (1 + (100 - min(iDaysSinceLastUpdate, 100)) / 100)
        repo._InnerSourceMetadata = repo._InnerSourceMetadata
        if repo._InnerSourceMetadata.get('participation'):
            iAverageCommitsPerWeek = repo._InnerSourceMetadata.get('participation')[:-13]
            iAverageCommitsPerWeek = reduce((lambda a,b: a + b), iAverageCommitsPerWeek) / 13
            print("Average commits per week: {0}".format(iAverageCommitsPerWeek))
            iScore = iScore * (1 + (min(max(iAverageCommitsPerWeek - 3, 0), 7)) / 7)

        iBoost = (1000 - min(iDaysSinceLastUpdate, 365) * 2.74)
        print("Boost 1: {0}".format(iBoost))
        iDaysSinceCreation = (time.time() - dp.parse(repo.created_at).timestamp()) / 86400
        print("Days Since Creation {0}".format(iDaysSinceCreation))
        iBoost *= (365 - min(iDaysSinceCreation, 365)) / 365
        print("Boost 2: {0}".format(iBoost))
        iScore += iBoost
        print("Score after applying boost: {0}".format(iScore))
        print("discription: {}",repo.description)
        if repo.description != None:
            if len(repo.description) > 30:
                print("hit 1")
                iScore += 50
            else:
                iScore += 0

        if repo._InnerSourceMetadata.get('guidelines') != None:
            if repo._InnerSourceMetadata.get('guidelines'):
                print("hit 2")
                iScore += 100
            else:
                iScore += 0

        if iScore > 3000:
            print("hit 3")
            iScore = 3000 + math.log(iScore) * 100

        iScore = round(iScore - 50)
        repo._InnerSourceMetadata['score'] = iScore
        print("Score final: {0}".format(iScore))
        return iScore
