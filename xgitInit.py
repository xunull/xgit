import requests
import os
import sys
import json
from yaml import load
from urllib.parse import urljoin

config = None

configPath = urljoin(__file__, './config.yml')

with open(configPath) as file:
    content = file.read()
    config = load(content)


def getGithubToken():
    githubToken = ''
    env_dist = os.environ
    if env_dist.get('github_token', None):
        githubToken = env_dist.get('github_token')
    else:
        githubToken = config['githubToken']

    return githubToken


def getGitlabToken():
    gitlabToken = ''
    env_dist = os.environ
    if env_dist.get('gitlab_token', None):
        gitlabToken = env_dist.get('gitlab_token')
    else:
        gitlabToken = config['gitlabToken']

    return gitlabToken


def createGithub(name):
    print("createGithub")
    headers = dict(Authorization="token " + getGithubToken())

    params = dict(name=str(name))

    r = requests.post(urljoin(config['githubUrl'], 'user/repos'),
                      data=json.dumps(params), headers=headers)

    if r.status_code == 201:
        print('github create success')
        projectUrl = config['githubRemoteUrl'].format(projectName=name)
        os.system('git remote add github {url}'.format(url=projectUrl))
    else:
        print(r.text)
        print('github create has error')


def createGitlab(name):
    print("createGitlab")
    headers = {
        "Private-Token": getGitlabToken()
    }

    params = dict(name=name)

    r = requests.post(urljoin(config['gitlabUrl'], 'projects'),
                      data=params, headers=headers)

    if r.status_code == 201:
        print('gitlab create success')
        projectUrl = config['gitlabRemoteUrl'].format(projectName=name)
        os.system('git remote add gitlab {url}'.format(url=projectUrl))
    else:
        print(r.text)
        print('gitlab create has error')


def initLocalGit():

    os.system('git init')


def create(initName):

    initLocalGit()
    createGithub(initName)
    createGitlab(initName)
