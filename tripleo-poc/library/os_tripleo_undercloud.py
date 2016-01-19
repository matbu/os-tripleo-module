#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""

DOCUMENTATION = '''
---
module: os-tripleo-undercloud
   - POC
options:
'''

EXAMPLES = '''

'''

import yum
import subprocess

class YumUtils(object):

    yb = None

    def __init__(self) :
        pass

    def yum_install(self, pkg):
        """ install package with the given package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.install(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def yum_remove(self, pkg):
        """ remove package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.remove(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def yum_update(self, pkg):
        """ update package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.update(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def _yum_manage(self, pkg, list='name'):
        """ manage yum packages """
        self.yb = yum.YumBase()
        searchlist=['name']
        arg=[pkg]
        return self.yb.searchGenerator(searchlist,arg)

class ShellUtils(object):

    def __init__(self):
        pass

    def _exec_shell_cmd(self, cmd):
        """ execute shell command """
        shell = subprocess.Popen(cmd,shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return shell.communicate()[0]

    def _exec_cmd(self, cmd):
        """ exec command without shell """
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        response = process.communicate()[0]
        return response

class Common(object):

    repo_path = "/etc/yum.repos.d/"

    def __init__(self):
        pass

    def set_repo(self, repos):
        for repo in repos:
            repo_name = repo.split('/')[len(repo.split('/'))-1]
            urllib.urlretrieve(repo, filename="%s%s" % (self.repo_path, repo_name))


class Undercloud(object):

    def __init__(self, user, repolist=None):
        self.user = user
        self.repolist = repolist
        self.yum = YumUtils()
        self.shell = ShellUtils()
        self.com = Common()

    def undercloud(self):
        self._install_pkg(['epel-release',])
        self.com.set_repo(['http://trunk.rdoproject.org/centos7/delorean-deps.repo',])
        self._install_pkg(['yum-plugin-priorities', 'python-tripleoclient',])
        self._install_undercloud()
        return self._get_instack_ip()

    def is_instack(self):
        if self._get_instack_ip() != '':
            return True

    def _install_pkg(self, pkgs):
        for pkg in pkgs:
            self.yum.yum_install(pkg)

    def _install_undercloud(self):
        return self.shell._exec_shell_cmd('su %s openstack undercloud install' % self.user)

    def _get_instack_ip(self):
        return self.shell._exec_shell_cmd("arp -n | grep virbr0 | awk '{print $1}'")


def _get_undercloud(module, kwargs):
    try:
        undercloud = Undercloud(user=kwargs.get('user') ,repolist=kwargs.get('repo'))
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)
    return provision

def _undercloud(module, kwargs):
    try:
        undercloud = _get_undercloud(module, kwargs)
        return os_undercloud.undercloud()
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)

def _is_undercloudk(module):
    undercloud = Undercloud()
    return undercloud.is_undercloud()

def main():
    argument_spec = (dict(
            repo                    = dict(Default=None),
            stack_user                    = dict(Default='stack'),
            state                   = dict(default='present', choices=['absent', 'present']),
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    if module.params['state'] == 'present':
        if _is_undercloud(module):
            module.exit_json(changed = False, result = "Success" )
        else:
            instack_ip = _provision(module, module.params)
            module.exit_json(changed = True, result = "Created" , ip = instack_ip)
    else:
        if _is_instack(module):
            module.exit_json(changed = True, result = "delete")
        else:
            module.exit_json(changed = False, result = "Success")

from ansible.module_utils.basic import *
from ansible.module_utils.shell import *
if __name__ == '__main__':
    main()
