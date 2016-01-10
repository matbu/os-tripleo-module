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
module: os-tripleo-privision
   - POC
options:
'''

EXAMPLES = '''

'''

class Provision(object):

    def __init__(self, repolist=None):
        self.repolist = repolist
        self.yum = YumUtils()
        self.shell = ShellUtils()
        self.com = Common()

    def provision(self):
        # run instack
        self.com.set_user('stack', 'stack')
        self.com.set_repo(['http://trunk.rdoproject.org/centos7/delorean-deps.repo',])
        self._install_pkg(['epel-release', 'instack-undercloud'])
        self._deploy_instack()
        return self._get_instack_ip()

    def is_instack(self):
        if self._get_instack_ip() != '':
            return True

    def _install_pkg(self, pkgs):
        for pkg in pkgs:
            self.yum.yum_install(pkg)

    def _deploy_instack(self):
        return self.shell._exec_shell_cmd('su stack instack-virt-setup')

    def _get_instack_ip(self):
        return self.shell._exec_shell_cmd("arp -n | grep virbr0 | awk '{print $1}'")


def _get_provision(module, kwargs):
    try:
        provision = Provision(repolist=kwargs.get('repo'))
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)
    return provision

def _provision(module, kwargs):
    try:
        os_provision = _get_provision(module, kwargs)
        return os_provision.provision()
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)

def _is_instack(module):
    provision = Provision()
    return provision.is_instack()

def main():
    argument_spec = (dict(
            repo                    = dict(Default=None),
            state                   = dict(default='present', choices=['absent', 'present']),
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    if module.params['state'] == 'present':
        if _is_instack(module):
            module.exit_json(changed = False, result = "Success" )
        else:
            instack_ip = _provision(module, module.params)
            module.exit_json(changed = True, result = "Created" , ip = instack_ip)
    else:
        if _is_instack(module):
            module.exit_json(changed = True, result = "delete")
        else:
            module.exit_json(changed = False, result = "Success")

# this is magic, see lib/ansible/module.params['common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
from library.utils.utils import YumUtils, ShellUtils
from library.utils.common import Common

if __name__ == '__main__':
    main()
