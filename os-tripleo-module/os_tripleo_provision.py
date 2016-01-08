#!/usr/bin/python
#coding: utf-8 -*-

from provision import Provision

DOCUMENTATION = '''
---
module: os-tripleo-privision
   - POC
options:
'''

EXAMPLES = '''

'''

def _get_provision(module, kwargs):
    try:
        provision = Provision(repolist=kwargs.get('repo'))
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)
    global _os_provision
    _os_provision = provision
    return provision

def _provision(module):
    try:
        return _os_provision.provision()
    except Exception, e:
        module.fail_json(msg = "Error : %s" %e.message)

def _is_instack(module):
    return _os_provision.is_instack()

def main():
    argument_spec = (dict(
            repo                    = dict(Default=None),
            state                   = dict(default='present', choices=['absent', 'present']),
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    provision = _get_provision(module, module.params)
    if module.params['state'] == 'present':
        if _is_instack(module):
            module.exit_json(changed = False, result = "Success" )
        else:
            instack_ip = _is_instack(module)
            module.exit_json(changed = True, result = "Created" , ip = instack_ip)
    else:
        if _is_instack(module):
            module.exit_json(changed = True, result = "delete")
        else:
            module.exit_json(changed = False, result = "Success")

# this is magic, see lib/ansible/module.params['common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
main()
