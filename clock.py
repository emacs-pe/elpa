#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
clock.py
========
A simple crontab for travis-ci.

Configuration
-------------
You need to get an travis-ci api key, see: http://docs.travis-ci.com/api/#authentication

    heroku create APP
    heroku config:set TRAVIS_API_KEY=MyTravisApiKey
    heroku config:set GITHUB_REPO_SLUG=emacs-pe/melpa
    heroku ps:scale clock=1
"""

from __future__ import print_function

import os

import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc

__version__ = '0.1'
TRAVIS_API_KEY = os.environ['TRAVIS_API_KEY']
GITHUB_REPO_SLUG = os.environ['GITHUB_REPO_SLUG']

scheduler = BlockingScheduler(timezone=utc)


@scheduler.scheduled_job('interval', hours=6)
def restart_last_build():
    print('Restarting last build of {0} at {1}'.format(GITHUB_REPO_SLUG, datetime.utcnow()))
    headers = {
        'Accept': 'application/vnd.travis-ci.2+json',
        'User-Agent': 'Clock/{0} travis-ci crontab'.format(__version__),
        'Authorization': 'token {0}'.format(TRAVIS_API_KEY),
    }
    resp_json = requests.get('https://api.travis-ci.org/repos/{0}/builds'.format(GITHUB_REPO_SLUG),
                             headers=headers).json()
    builds = resp_json['builds']
    last_build = builds and builds[0]
    if not last_build:
        return
    resp_json = requests.post('https://api.travis-ci.org/builds/{0}/restart'.format(last_build['id']),
                              headers=headers).json()
    print('Correctly restarted: {0}'.format(resp_json['result']))


if __name__ == '__main__':
    scheduler.start()
