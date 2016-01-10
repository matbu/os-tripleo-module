#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Product name: os-tripleo-module
    Copyright (C) matbu 2016
    Author(s): Mathieu BULTEL
    Description : Deploy tools
"""
import mock
import yaml

class FakeVirtHost(object):

    instack_ip = '192.168.122.95'

    def get_instack_ip():
        return self.instack_ip

    create_server = mock.MagicMock()
