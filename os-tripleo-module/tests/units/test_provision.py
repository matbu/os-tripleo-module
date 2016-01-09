#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""

from tests.units.fakes import FakeVirtHost
import os_tripleo_provision_test

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

class TestProvision(object):
    '''This class exercises the _network_args function of the
    os_server module.  For each test, we parse the YAML document
    contained in the docstring to retrieve the module parameters for the
    test.'''

    def setup_method(self, method):
        self.virthost = FakeVirtHost()
        self.module = mock.MagicMock()
        self.module.params = params_from_doc(method)

    @mock.patch.object(os_tripleo_provision_test, '_is_instack')
    def test_is_instack_exist(self, mock_tripleo):
        '''
        - os_tripleo_provision_test:
            repo: ['http://rdo.repo.org']
        '''
        mock_tripleo._is_instack.return_value = self.virthost.get_instack_ip()
        instack_ip = os_tripleo_provision_test._is_instack(self.module)
        self.assertEqual(mock_tripleo, instack_ip)
