#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""
from utils import ShellUtils
import urllib

class Common(object):

    repo_path = "/etc/yum.repos.d/"

    def __init__(self):
        pass

    def set_user(self, user, pwd):
        pass
#        sudo useradd stack
#        sudo passwd stack  # specify a password
#        echo "stack ALL=(root) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/stack
#        sudo chmod 0440 /etc/sudoers.d/stack

    def set_repo(self, repos):
        for repo in repos:
            repo_name = repo.split('/')[len(repo.split('/'))-1]
            urllib.urlretrieve(repo, filename="%s%s" % (self.repo_path, repo_name))
