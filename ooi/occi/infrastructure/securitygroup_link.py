# -*- coding: utf-8 -*-

# Copyright 2015 LIP - INDIGO-DataCloud
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ooi.occi.core import attribute as attr
from ooi.occi.core import kind
from ooi.occi.core import link
from ooi.occi import helpers


class SecurityGroupLink(link.Link):
    attributes = attr.AttributeCollection([])
    kind = kind.Kind(helpers.build_scheme('infrastructure'),
                     'securitygrouplink', 'security group link resource',
                     attributes, 'securitygrouplink/',
                     related=[link.Link.kind])

    def __init__(self, mixins, source, target, id=None):

        super(SecurityGroupLink, self).__init__(None, mixins, source,
                                               target, id)