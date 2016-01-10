#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""

from os_tripleo_module.tests.units.fakes import FakeVirtHost
from os_tripleo_module import os_tripleo_provision_test

class AnsibleFail(Exception):
    pass


class AnsibleExit(Exception):
    pass

def params_from_doc(func):
    '''This function extracts the docstring from the specified function,
    parses it as a YAML document, and returns parameters for the
    os_tripleo_provision module.'''

    doc = inspect.getdoc(func)
    cfg = yaml.load(doc)

    for task in cfg:
        for module, params in task.items():
            for k, v in params.items():
                if k in ['nics'] and type(v) == str:
                    params[k] = [v]
        task[module] = collections.defaultdict(str,
                                               params)

    return cfg[0]['os_tripleo_provision_test']

class test_provision(object):
    '''This class exercises the _network_args function of the
    os_server module.  For each test, we parse the YAML document
    contained in the docstring to retrieve the module parameters for the
    test.'''

    def setup_method(self, method):
        self.virthost = FakeVirtHost()
        self.module = mock.MagicMock()
        self.module.params = params_from_doc(method)

    @mock.patch.object(os_tripleo_provision_test, '_is_instack')
    @mock.patch('os_tripleo_module.os_tripleo_provision_test.AnsibleModule')
    def test_is_instack_exist(self, mock_tripleo, mock_module):
        '''
        - os_tripleo_provision_test:
            repo: ['http://rdo.repo.org']
        '''
        instance = mock_module.return_value
        mock_tripleo._is_instack.return_value = '192.168.122.95'
        os_tripleo_provision_test.main()
        assert_equals(instance.exit_json.call_count, 0)
