#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""

import mock
from library import os_tripleo_provision
from library.os_tripleo_provision import Provision
from nose.tools import assert_equals, set_trace

@mock.patch('library.os_tripleo_provision.Provision._get_instack_ip')
@mock.patch('library.os_tripleo_provision.AnsibleModule')
def test_is_instack_exist(mock_module, mock_provision):
    '''
    - os_tripleo_provision:
        repo: ['http://rdo.repo.org']
    '''
    mock_provision.return_value = '192.168.122.95'
    result = os_tripleo_provision._is_instack(mock_module)
    assert_equals(result, True)
