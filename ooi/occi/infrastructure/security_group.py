# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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
from ooi.occi.core import resource
from ooi.occi import helpers


class SecurityGroup(resource.Resource):
    attributes = attr.AttributeCollection(["occi.securitygroup.rules"])
    kind = kind.Kind(helpers.build_scheme('infrastructure'), 'securitygroup',
                     'security group resource', attributes, 'securitygroup/',
                     related=[resource.Resource.kind])

    def __init__(self, title, id, rules, summary=None, mixins=[]):
        super(SecurityGroup, self).__init__(title, mixins, summary=summary,
                                            id=id)
        self.attributes["occi.securitygroup.rules"] = attr.MutableAttribute(
            "occi.securitygroup.rules", rules)

    @property
    def rules(self):
        return self.attributes["occi.securitygroup.rules"].value

    @rules.setter
    def rules(self, value):
        self.attributes["occi.securitygroup.rules"].value = value